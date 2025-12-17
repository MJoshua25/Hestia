from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        # Auto-clean old notifications (older than 60 days)
        cutoff_date = timezone.now() - timedelta(days=60)
        Notification.objects.filter(user=self.request.user, created_at__lt=cutoff_date).delete()
        
        queryset = Notification.objects.filter(user=self.request.user)
        filter_type = self.request.GET.get('filter')
        
        if filter_type == 'unread':
            queryset = queryset.filter(is_read=False)
        elif filter_type in Notification.Type.values:
            queryset = queryset.filter(type=filter_type)
            
        return queryset

@require_GET
def get_unread_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0, 'notifications': []})
    
    # Get unread notifications count
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    # Get latest 5 notifications
    latest = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    data = []
    for notif in latest:
        data.append({
            'id': notif.id,
            'type': notif.type,
            'title': notif.title,
            'message': notif.message[:50] + '...' if len(notif.message) > 50 else notif.message,
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_read': notif.is_read,
            'icon': notif.icon,
            'link': notif.link
        })
        
    return JsonResponse({'count': count, 'notifications': data})

@require_POST
def mark_as_read(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'}, status=403)
        
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'status': 'success'})

@require_POST
def mark_all_as_read(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'}, status=403)
        
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@require_POST
def delete_notification(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'}, status=403)
        
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return JsonResponse({'status': 'success'})

@require_POST
def toggle_read_status(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'}, status=403)
        
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = not notification.is_read
    notification.save()
    
    return JsonResponse({'status': 'success', 'is_read': notification.is_read})
