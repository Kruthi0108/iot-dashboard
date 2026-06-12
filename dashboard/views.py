from django.shortcuts import (
    render,
    redirect
)

from django.http import HttpResponse

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)

from django.contrib.auth.decorators import (
    login_required
)

from .models import SensorData

import random
import csv


def login_page(request):

    # auto-create admin user if not exists
    User = get_user_model()

    if not User.objects.filter(
        username='admin'
    ).exists():

        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin123'
        )

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

    return render(
        request,
        'login.html'
    )


def logout_page(request):

    logout(request)

    return redirect(
        'login'
    )


@login_required
def home(request):

    temperature = random.randint(
        20,
        40
    )

    humidity = random.randint(
        40,
        90
    )

    device_status = random.choice([
        'ON',
        'OFF'
    ])

    SensorData.objects.create(
        temperature=temperature,
        humidity=humidity,
        device_status=device_status
    )

    latest_data = (
        SensorData.objects
        .all()
        .order_by(
            '-created_at'
        )[:10]
    )

    temperature_data = [
        item.temperature
        for item in latest_data
    ][::-1]

    humidity_data = [
        item.humidity
        for item in latest_data
    ][::-1]

    avg_temp = round(
        sum(temperature_data)
        / len(temperature_data),
        2
    )

    highest_temp = max(
        temperature_data
    )

    lowest_temp = min(
        temperature_data
    )

    if temperature > 35:

        alert = (
            "⚠ High Temperature!"
        )

        temp_color = "red"

    else:

        alert = (
            "✅ Temperature Normal"
        )

        temp_color = "green"

    context = {

        'temperature':
        temperature,

        'humidity':
        humidity,

        'device_status':
        device_status,

        'temp_color':
        temp_color,

        'alert':
        alert,

        'temperature_data':
        temperature_data,

        'humidity_data':
        humidity_data,

        'sensor_history':
        latest_data,

        'avg_temp':
        avg_temp,

        'highest_temp':
        highest_temp,

        'lowest_temp':
        lowest_temp
    }

    return render(
        request,
        'dashboard.html',
        context
    )


def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="sensor_data.csv"'
    )

    writer = csv.writer(
        response
    )

    writer.writerow([
        'Temperature',
        'Humidity',
        'Status',
        'Time'
    ])

    data = (
        SensorData.objects
        .all()
    )

    for sensor in data:

        writer.writerow([
            sensor.temperature,
            sensor.humidity,
            sensor.device_status,
            sensor.created_at
        ])

    return response