
#!/usr/bin/env python3

from .forms import UserForm,UserProfileInfoForm
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings as django_settings
import os
import mimetypes
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper


# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Import the database table models and form

# Create your views here.
def index(request):
    return render(request,'index.html')


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basicapp/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})

from .forms import FormnewuserForm

def showform(request):
    form= FormnewuserForm(request.POST or None)
    if form.is_valid():
        form.save()
    context= {'form': form }

    return render(request, 'newuserform.html', context)





# Database Connection Code .
import mysql.connector
#connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user>
#print('Successfully connected to database')
#cursor = connection.cursor()
def data_read(dev_loc,cap_num):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor= connection.cursor()
    blob_query ="SELECT *from %s where cap_id ='%s'"%(dev_loc,cap_num)
    cursor.execute(blob_query)
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    return record

def data_list(cp_dt,cap_loc):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    cur_input ="select cap_id from %s where Date='%s'"%(cap_loc,cp_dt)
    print(cur_input)
    cursor.execute(cur_input)
    data = cursor.fetchall()
    print(list(data))
    cursor.close()
    connection.close()
    print("End of Data List ")
    return data

def scan_list(cap_loc):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    cur_input="select cap_id from %s ORDER BY cap_id  DESC LIMIT 1"%(cap_loc)
    print(cur_input)
    cursor.execute(cur_input)
    data1 = cursor.fetchall()
    str_tup = str(data1)
    data=str_tup[2:14]

    #data = int(filter(str.isdigit, data_1))
    print(data)
    cursor.close()
    connection.close()
    print("End of Data List ")
    return data

def dev_loc():
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    cur_input ="show tables LIKE '%tshark%'"
    cursor.execute(cur_input)
    data = cursor.fetchall()
    print(list(data))
    cursor.close()
    connection.close()
    return data

def home(request):
    data=[]
    loc = dev_loc()
    global cap_dev

    if request.method == 'POST':
        cap_date = request.POST.get('cap_date')
        cap_dev =  request.POST.get('cap_loc')
        data =     data_list(cap_date,cap_dev)
        #cap_time = request.POST.get('cap_sec')
        #scan_cap(cap_time)

    return render(request,'home.html',{'datacapture':data,'devicelocation':loc})

import datetime
import time

def scan(request):
    data= 0
    loc = dev_loc()
    global cap_dev

    if request.method == 'POST':
        cap_date = datetime.datetime.today().strftime("%Y-%m-%d")
        print(cap_date)
        cap_dev =  request.POST.get('dev_loc')
        #data =     data_list(cap_date,cap_dev)
        cap_time = request.POST.get('cap_sec')
        scan_cap(cap_dev,cap_time)
        ts=int(cap_time)+5
        time.sleep(ts) # Sleep for 15 seconds
        data = scan_list(cap_dev)
        print(data)
    return render(request,'scan.html',{'datacapture':data,'devicelocation':loc})


def download_pcap(request):
    cap_id=request.POST.get('cap_id')
    download_cap(cap_id)
    cap_name = "data_capture_%s.pcap"%(cap_id)
    print(cap_name)
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    f_nm = "%s/data_capture_%s.pcap"%(f_path,cap_id)
    capfile=cap_name
    filename = f_nm
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/pcap')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(capfile +".pcap")
    return response



def download_cap(cap_num):
    #cap_dev = 'tshark_loc1'
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    tshark_data = "%s/data_capture_%s.pcap"%(f_path,cap_num)
    record=data_read(cap_dev,cap_num)
    for row in record:
        print("Id = ", row[0])
        tshark_file = row[1]
        print("Storing the captured data on the local disk \n")
        write_file(tshark_file, tshark_data)



def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


import paramiko

def scan_cap(cap_dev,cap_time):
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    cap_loc=cap_dev
    ip_addr={"tshark_db_table" :"10.8.0.6","tshark_Jeyasekharan" : "10.8.0.10"}
    for field, value in ip_addr.items():
        if field == cap_loc:
            host_id = ip_addr[field]

    print(host_id)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host_id, username="ubuntu", password="Pa$$w0rd")
        print("Client is connected")
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    client_cmd= "python3 /home/ubuntu/python_scan.py %s"%(cap_time)
    print(client_cmd)
    client.exec_command(client_cmd)
    # close the connection
    client.close()


def scan_download_pcap(request):
    cap_id= scan_list(cap_dev)
    download_cap(cap_id)
    cap_name = "data_capture_%s.pcap"%(cap_id)
    print(cap_name)
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    f_nm = "%s/data_capture_%s.pcap"%(f_path,cap_id)
    capfile=cap_name
    filename = f_nm
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/pcap')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(capfile +".pcap")
    return response


def download_nmap(request):
    #nmap_id=request.POST.get('nmap_id')
    nmap_id = nmap_list(nmap_dev)
    download_map(nmap_id)
    nmap_name = "nmap_%s.txt"%(nmap_id)
    print(nmap_name)
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    f_nm = "%s/nmap_%s.txt"%(f_path,nmap_id)
    nmapfile=nmap_name
    filename = f_nm
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/txt')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(nmapfile+".txt")
    return response



def download_map(nmap_num):
    #cap_dev = 'tshark_loc1'
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    nmap_data = "%s/nmap_%s.txt"%(f_path,nmap_num)
    record=nmap_read(nmap_dev,nmap_num)
    for row in record:
        print("Id = ", row[0])
        nmap_file = row[1]
        print("Storing the captured data on the local disk \n")
        write_file(nmap_file,nmap_data)



def nmapscan(request):
    data= 0
    #nmap_ip=0
    loc = nmap_loc()
    nmap_int_nm=[]
    global nmap_dev

    if request.method == 'POST':
        nmap_date = datetime.datetime.today().strftime("%Y-%m-%d")
        print(nmap_date)
        #print(nmap_dev)
        nmap_dev =  request.POST.get('dev_loc')
        print(nmap_dev)
        nmap_int_nm=nmap_net_inf(nmap_dev)
        nm_ip = request.POST.get('nmapip')
        sb_ip= request.POST.get('nmapsubnet')
        scan_nmap(nm_ip,sb_ip)
        ts=15
        time.sleep(ts) # Sleep for 5 seconds
        data = nmap_list(nmap_dev)
        print(data)
        scan_nmap_dev()

    return render(request,'nmap_scan.html',{'datacapture':data,'devicelocation':loc,'Interface_name':nmap_int_nm})
    #return render(request,'nmap_scan.html',{'datacapture':data,'devicelocation':loc,'Interface_name':nmap_int_nm})



def scan_nmap(nm_ipaddr,sub_addr):
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    cap_loc=nmap_dev
    ip_addr={"nmap_loc1" :"10.8.0.6","nmap_Jeyasekharan" : "10.8.0.10"}
    for field, value in ip_addr.items():
        if field == cap_loc:
            host_id = ip_addr[field]

    print(host_id)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host_id, username="ubuntu", password="Pa$$w0rd")
        print("Client is connected")
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    nmap_id =nm_ipaddr
    sub_id = sub_addr
    print(sub_id)
    if bool(sub_id):
        client_cmd= "python3 /home/ubuntu/nmap_scan.py %s/%s"%(nmap_id,sub_id)
        print(client_cmd)
    else:
        client_cmd= "python3 /home/ubuntu/nmap_scan.py %s"%(nmap_id)
        print(client_cmd)
    client.exec_command(client_cmd)
    # close the connection
    client.close()


def nmap_list(nmap_loc):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    cur_input="select nmap_id from %s ORDER BY nmap_id  DESC LIMIT 1"%(nmap_loc)
    print(cur_input)
    cursor.execute(cur_input)
    data1 = cursor.fetchall()
    str_tup = str(data1)
    data=str_tup[2:14]

    #data = int(filter(str.isdigit, data_1))
    print(data)
    cursor.close()
    connection.close()
    print("End of Data List ")
    return data

def nmap_loc():
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    cur_input ="show tables LIKE '%nmap%'"
    cursor.execute(cur_input)
    data = cursor.fetchall()
    print(list(data))
    cursor.close()
    connection.close()
    return data

def nmap_net_inf(dev_name):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor = connection.cursor()
    loc_intf=dev_name
    cur_input ="select int_name,INET_NTOA(IPV4Addr) from %s_int ORDER BY Nmap_date DESC LIMIT 3 ;"%(loc_intf)
    cursor.execute(cur_input)
    data = cursor.fetchall()
    print(list(data))
    cursor.close()
    connection.close()
    return data


def nmap_read(dev_loc,nmap_num):
    connection = mysql.connector.connect(host='167.71.236.9',database='tshark_db',user='mysqltest',password='Pa$$w0rd')
    print('Successfully connected to database')
    cursor= connection.cursor()
    blob_query ="SELECT *from %s where nmap_id ='%s'"%(dev_loc,nmap_num)
    cursor.execute(blob_query)
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    return record


def view_nmap(request):
    #nmap_id=request.POST.get('nmap_id')
    nmap_id = nmap_list(nmap_dev)
    download_map(nmap_id)
    nmap_name = "nmap_%s.txt"%(nmap_id)
    print(nmap_name)
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    f_nm = "%s/nmap_%s.txt"%(f_path,nmap_id)
    nmapfile=nmap_name
    filename = f_nm
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/txt')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(nmapfile+".txt")
    return response

def view_pcap(request):
    cap_id= scan_list(cap_dev)
    download_cap(cap_id)
    cap_name = "data_capture_%s.pcap"%(cap_id)
    print(cap_name)
    f_path =os.path.join(django_settings.STATIC_ROOT)
    print(f_path)
    f_nm = "%s/data_capture_%s.pcap"%(f_path,cap_id)
    capfile=cap_name
    filename = f_nm
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/pcap')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(capfile +".pcap")
    return response

# Client Registration
from .forms import ClientForm
from .models import Client
from django.contrib import messages
from django.core.paginator import Paginator

from django.core import serializers
from django.http import JsonResponse

def client_show(request):
    if 'q' in request.GET:
        q=request.GET['q']
        clients=Client.objects.filter(client_name__icontains=q)
    else:
        clients=Client.objects.all()
    # Pagintion
    paginator=Paginator(clients,4)
    page_number=request.GET.get('page')
    clients_obj=paginator.get_page(page_number)
    return render(request,'client_show.html',{'clients':clients_obj})


def client(request):
        if request.method == "POST":
                form = ClientForm (request.POST) # here "form" is one variable
                print(form)
                if form.is_valid():
                        try:
                                form.save()
                                return redirect("/basicapp/client_show")
                        except:
                                pass
        else:
                form = ClientForm()
        return render(request,"client_index.html",{'form':form})



#def client_show(request):
#        clients = Client.objects.all() # it's select query,select all data store in clientss variable
#        paginator=Paginator(clients,3)
#        page_number=request.GET.get('page')
#        clients=paginator.get_page(page_number)
#        return render(request,"client_show.html",{'clients': clients})


def client_edit(request,id):
        client = Client.objects.get(id=id)
        print(client)
        return render(request,"client_edit.html",{'client':client})


def client_update(request,id):
        client = Client.objects.get(id=id)
        form = ClientForm(request.POST, instance=client)
        print(form)
        if form.is_valid():
                form.save()
                print("Form Saved")
                return redirect("/basicapp/client_show")
        print("Form not saved")
        return render(request,"client_edit.html",{'client':client})


def client_delete(request,id):
        client = Client.objects.get(id=id)
        client.delete()
        return redirect("/basicapp/client_show")

def client_home(request):
        return render(request,"client_home.html")


def scan_nmap_dev():
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    cap_loc=nmap_dev
    ip_addr={"nmap_loc1" :"10.8.0.6","nmap_Jeyasekharan" : "10.8.0.10"}
    for field, value in ip_addr.items():
        if field == cap_loc:
            host_id = ip_addr[field]

    print(host_id)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host_id, username="ubuntu", password="Pa$$w0rd")
        print("Client is connected")
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    client_cmd= "python3 /home/ubuntu/nmap_device_scan.py"
    print(client_cmd)
    client.exec_command(client_cmd)
    # close the connection
    client.close()



from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from basicapp.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
