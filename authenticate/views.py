from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Concert
from .models import ConcertSeat
from .models import Transaction
from .models import TransactionTicket
from django.db.models import Sum
from .models import ExtendUser
import ast
from django.urls import reverse

# Create your views here.
def homepage(request):
    return  render(request, "authenticate/firstpage.html")


def signup(request):
    if request.method=="POST":
        username= request.POST.get('urname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email= request.POST.get('email')
        p1 = request.POST.get('p1')
        p2 = request.POST.get('p2')
        theuser = User.objects.create_user(username,email, p1)
        extended_user = ExtendUser()
        extended_user.user = theuser
        extended_user.balance = 500
        theuser.first_name = fname
        theuser.last_name = lname
        theuser.save()
        extended_user.save()
        messages.success(request,"Account created successfully")
        return redirect('signin')
    return render(request, "authenticate/signup.html", {"error": True})


def signin(request):
    if request.method=="POST":
        uname= request.POST['uname']
        p1= request.POST['p1']
        user = authenticate(username=uname, password=p1)
        if user is not None:
            login(request,user)
            return redirect('ticket')
        else:
            messages.error(request, "Credentials not valid")
            return redirect('signin')
    return render(request, "authenticate/signin.html")


def signout(request):
    logout(request)
    return redirect('homepage')


def payment(request):
    return render(request, "authenticate/payment.html")


def ticket(request):
    current_user = request.user
    concerts = Concert.objects.all()
    return render(request,'authenticate/ticket.html', {'concerts':concerts, 'user': current_user})


def concert_details(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    context = {'concert': concert, 'user': request.user, 'seats': concert.seats.all(), 'transaction_complete':True, 'can_buy':True}
    return render(request, 'authenticate/paymentform.html', context)


def success(request, concert_id):
    tid = int(request.GET['trans_id'])
    transaction = Transaction.objects.get(id=tid)
    transaction_tickets = transaction.transactionticket_set.all()
    data = []

    for ticket in transaction_tickets:
        d = {'id': ticket.id, 'type': ticket.seat.name, 'amount': ticket.count, 'price': ticket.seat.price, 'seats_price': ticket.seat.price * ticket.count}
        data.append(d)

    context = {
        'trans_id': request.GET['trans_id'],
        'total': transaction.total_cost,
        'balance': request.user.extenduser.balance,
        'data': data,
    }

    return render(request, "authenticate/success.html", context) 


def transaction_post(request, concert_id):
    if request.method == "POST":
        # process transaction
        balance = request.user.extenduser.balance
        total = float(request.POST['total'])
        context = {
            'sub_total': request.POST['sub_total'],
            'total': request.POST['total'],
            'transaction_complete':False,
            'balance': float(request.user.extenduser.balance),
            'after_balance': float(request.user.extenduser.balance) - total,
            'no_funds':True,
            'data': ast.literal_eval(request.POST['data']),
            'can_buy':True,
        }

        if 'transaction_complete' in request.POST:
            if request.POST['transaction_complete']:
                print('dont repeat')
                return render(request, "authenticate/checkout.html", context)
        
        # calculate if seats are vailable
        seats = context['data']
        can_buy = True
        for seat in seats:                
            ticket_obj = ConcertSeat.objects.get(id=int(seat['id']))
            if ticket_obj.occupancy - seat['amount'] < 0:
                can_buy = False
                break
            
        if (total > balance):
            return render(request, "authenticate/checkout.html", context)
        elif can_buy:
            # save transaction to db
            transaction = Transaction(
                user=request.user,
                total_cost=total,
                concert=Concert.objects.get(id=concert_id)
            )
            transaction.save()

            # remove total from balance
            extend_user = request.user.extenduser
            extend_user.balance = extend_user.balance - total
            extend_user.save()
            # subtract all tickets counts from concertseats
            tickets = context['data']
            for ticket in tickets:                
                ticket_obj = ConcertSeat.objects.get(id=int(ticket['id']))
                ticket_obj.occupancy = ticket_obj.occupancy - ticket['amount']
                ticket_obj.save()
            
            #save tickets to transaction ticket
            for ticket in tickets:
                seat = ConcertSeat.objects.get(id=int(ticket['id']))
                trans_ticket = TransactionTicket(
                    transaction=transaction,
                    seat = seat,
                    count=ticket['amount']
                )
                trans_ticket.save()

            context['no_funds'] = False
            context['transaction_complete'] = True
            context['trans_id'] = transaction.id
            context['can_buy'] = True

            return redirect(reverse('success', kwargs={'concert_id': concert_id}) + "?trans_id=" + str(transaction.id))

    return render(request, "authenticate/checkout.html", context)
    

def payment_post(request, concert_id):
    if request.method == "POST":
        print(request.POST.dict())
        concert = get_object_or_404(Concert, id=concert_id)
        seats = concert.seats.all()
        data = []
        # get all selected tickets
        for i in range(len(seats)):
            name = str(seats[i].name)
            num = int(request.POST[name])
            if seats[i].occupancy > 0 and num > 0:
                data.append({'id': seats[i].id, 'type': seats[i].name, 'amount': num, 'price': seats[i].price})
        # see if they can afford it
        total_price = 0
        for seat in data:
            total_price = total_price + float(seat['price']) * float(seat['amount'])
        total_tax = total_price * 1.14

        context = {
            'data': data,
            'sub_total': total_price,
            'total': total_tax,
            'transaction_complete':False,
            'balance': float(request.user.extenduser.balance),
            'after_balance': float(request.user.extenduser.balance) - total_tax,
            'no_funds':False,
            'can_buy':True
        }
        # calculate if seats are vailable
        seats = context['data']
        can_buy = True
        for seat in seats:                
            ticket_obj = ConcertSeat.objects.get(id=int(seat['id']))
            if ticket_obj.occupancy - seat['amount'] < 0:
                can_buy = False
                break
        
        context['can_buy'] = can_buy

        if (total_price != 0 and can_buy):
            return render(request, "authenticate/checkout.html", context)
        else:
            return render(request, "authenticate/paymentform.html", context)
    
    # idk if this is needed but im not gonna touch it
    concert = get_object_or_404(Concert, id=concert_id)
    context = {'concert': concert, 'user': request.user, 'seats': concert.seats.all()}

    return render(request, "authenticate/paymentform.html", context)


def profile(request):
    context = {
        'transactions': []
    }

    transactions = request.user.transaction_set.all()

    for transaction in transactions:
        t = {
            'trans_id': transaction.id,
            'seats': [],
            'total': transaction.total_cost,
            'concert': transaction.concert
        }
        transaction_tickets = transaction.transactionticket_set.all()
        for ticket in transaction_tickets:
            t['seats'].append({'id': ticket.id, 'type': ticket.seat.name, 'amount': ticket.count, 'price': ticket.seat.price, 'seats_price': ticket.seat.price * ticket.count})
        context['transactions'].append(t)
        

    return render(request, "authenticate/profile.html", context)