from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Shipment


def index(request):
    """Render home page"""
    return render(request, 'index.html')


def signin(request):
    """Render sign in page"""
    return render(request, 'signin.html')


def signup(request):
    """Render sign up page"""
    return render(request, 'signup.html')


def track_page(request):
    """Renders the tracking page with map and timeline"""
    return render(request, "track.html")


def shipment_detail_json(request, tracking_number):
    """Returns full shipment details as JSON with optimized queries"""
    try:
        # Use prefetch_related to avoid N+1 queries on events
        shipment = Shipment.objects.prefetch_related('events').get(tracking_number=tracking_number)
        response = JsonResponse(shipment.to_dict())
        # Add cache headers - cache for 5 minutes (300 seconds)
        response['Cache-Control'] = 'public, max-age=300'
        return response
    except Shipment.DoesNotExist:
        return JsonResponse({"error": "Tracking number not found"}, status=404)


def shipment_location_json(request, tracking_number):
    """Returns only current location and status as JSON (lighter weight)"""
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    data = {
        "tracking_number": shipment.tracking_number,
        "current_lat": shipment.current_lat,
        "current_lng": shipment.current_lng,
        "status": shipment.status,
        "progress": shipment.progress_percentage(),
    }
    response = JsonResponse(data)
    # Cache location data for 2 minutes (shorter than full details)
    response['Cache-Control'] = 'public, max-age=120'
    return response


def shipments_list(request):
    """Returns paginated list of shipments (optimized)"""
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 20)
    
    try:
        page = int(page)
        limit = int(limit)
        limit = min(limit, 100)  # Cap at 100 to prevent abuse
    except ValueError:
        page = 1
        limit = 20
    
    offset = (page - 1) * limit
    # Use only() to select specific fields - reduces DB load
    shipments = Shipment.objects.only(
        'tracking_number', 'status', 'origin', 'destination', 'created_at'
    )[offset:offset + limit]
    total = Shipment.objects.count()
    
    data = {
        "total": total,
        "page": page,
        "limit": limit,
        "shipments": [
            {
                "tracking_number": s.tracking_number,
                "status": s.status,
                "origin": s.origin,
                "destination": s.destination,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for s in shipments
        ]
    }
    return JsonResponse(data)
