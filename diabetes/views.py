import random
from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Avg
from django.db.models.functions import TruncMinute, TruncSecond
from django.shortcuts import render
from numpy import *
from sklearn import *

from diabetes.models import UserProfile, GlucoseData, DiabetesTypeChoices, GenderChoices


def get_recommendations(request):
    interval = int(request.GET.get('interval', 1))
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.diabetes_type == DiabetesTypeChoices.type_1:
        base_glucose_level = 100
        fluctuation_range = 30
    else:
        base_glucose_level = 120
        fluctuation_range = 20
    if user_profile.gender == GenderChoices.female:
        base_glucose_level -= 10
        fluctuation_range -= 5
        if user_profile.pregnancy_status:
            base_glucose_level += 20
            fluctuation_range += 10
    glucose_fluctuation = random.randint(-fluctuation_range, fluctuation_range)
    glucose_level = base_glucose_level + glucose_fluctuation
    glucose_level = max(70, min(glucose_level, 250))
    GlucoseData.objects.create(
        user_profile=user_profile,
        glucose_level=glucose_level,
        timestamp=datetime.now()
    )
    if interval == 1:
        every = 5
    elif interval == 5:
        every = 60
    elif interval == 10:
        every = 120
    elif interval == 15:
        every = 180
    if interval > 1:
        glucose_levels = GlucoseData.objects.filter(
            user_profile=user_profile,
            timestamp__gte=datetime.now() - timedelta(minutes=interval)
        ).annotate(minute=TruncMinute('timestamp')).values('minute', 'glucose_level').order_by('minute')
    else:
        glucose_levels = GlucoseData.objects.filter(
            user_profile=user_profile,
            timestamp__gte=datetime.now() - timedelta(minutes=interval)
        ).annotate(minute=TruncSecond('timestamp')).values('minute', 'glucose_level').order_by('minute')

    average_glucose_level = GlucoseData.objects.filter(
        user_profile=user_profile,
        timestamp__gte=datetime.now() - timedelta(minutes=interval)
    ).aggregate(Avg('glucose_level'))['glucose_level__avg']
    data = [glucose_level['glucose_level'] for glucose_level in glucose_levels]
    data = array(data)
    data = data.reshape(-1, 1)
    # clean the data
    scaler = preprocessing.StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)
    # predict the action
    model = linear_model.LinearRegression()
    model.fit(data, data)
    prediction = model.predict(data)
    prediction = scaler.inverse_transform(prediction)
    prediction = prediction[-1][0]
    if prediction > 150:
        messages.error(request,
                       f'Our Algorithm predicts that your glucose level will rise in the next {interval} {"minutes" if interval > 1 else "minute"}, please take insulin')
    elif prediction < 70:
        messages.error(request,
                       f'Our Algorithm predicts that your glucose level will drop in the next {interval} {"minutes" if interval > 1 else "minute"}, please eat something')

    return render(request, 'recommendations.html', {
        'glucose_levels': glucose_levels,
        'average_glucose_level': average_glucose_level,
        'interval': interval,
        'every': every,
        'prediction': prediction
    })
