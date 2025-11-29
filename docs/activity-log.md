# Activity Log Design Documentation

## Overview
Sistem activity log untuk mencatat semua aktivitas user dan guest terhadap data dalam aplikasi (create, update, delete, dll). Desain ini menggunakan satu tabel dengan struktur fleksibel untuk mendukung berbagai jenis entitas dan actor (user atau guest).

## Database Schema

### Tabel: `activity_logs`

```sql
CREATE TABLE activity_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- Actor Information (User atau Guest)
    user_id BIGINT NULL,
    actor_type VARCHAR(5) NOT NULL DEFAULT 'user',  -- Optimized for enum
    actor_identifier VARCHAR(255),
    actor_name VARCHAR(255),
    actor_metadata JSON,

    -- Activity Information
    action VARCHAR(12) NOT NULL,  -- Enum-based actions
    entity VARCHAR(50) NOT NULL,  -- Simple entity type
    computed_entity VARCHAR(100) NOT NULL,  -- Full model path (app_label.ModelName)
    entity_id BIGINT,
    entity_name VARCHAR(255),

    -- Change Details
    old_values JSON,
    new_values JSON,
    changed_fields JSON,

    -- Metadata
    description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    extra_data JSON,  -- NEW: Flexible storage for additional context

    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Relations & Indexes (MySQL Safe Configuration)
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_actlog_created_at (created_at DESC),
    INDEX idx_actlog_type_time (actor_type, created_at DESC),
    INDEX idx_actlog_entity (entity, entity_id),
    INDEX idx_actlog_comp_ent (computed_entity, entity_id),
    INDEX idx_actlog_action_time (action, created_at DESC),
    INDEX idx_actlog_actor_id (actor_identifier),
    INDEX idx_actlog_ent_time (entity, created_at DESC)
);
```

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | BIGINT | Primary key, auto increment |
| `user_id` | BIGINT | Foreign key ke tabel users, NULL jika guest |
| `actor_type` | VARCHAR(5) | Tipe actor dari enum: `user` atau `guest` |
| `actor_identifier` | VARCHAR(255) | Identifier unik: email, phone, session_id, atau IP |
| `actor_name` | VARCHAR(255) | Nama actor (user name atau guest name) |
| `actor_metadata` | JSON | Data tambahan actor (untuk guest: email, phone, device, dll) |
| `action` | VARCHAR(12) | Jenis aktivitas dari ActionType enum: `create`, `update`, `delete`, `view`, `login`, dll |
| `entity` | VARCHAR(50) | Tipe entitas sederhana: `product`, `order`, `user`, dll |
| `computed_entity` | VARCHAR(100) | **BARU:** Path model lengkap untuk import langsung: `core.Product`, `auth.User` |
| `entity_id` | BIGINT | ID dari entitas yang diakses |
| `entity_name` | VARCHAR(255) | Nama/title entitas untuk display di UI |
| `old_values` | JSON | Snapshot data sebelum perubahan |
| `new_values` | JSON | Snapshot data setelah perubahan |
| `changed_fields` | JSON | Array field yang berubah |
| `description` | TEXT | Deskripsi human-readable untuk UI |
| `ip_address` | VARCHAR(45) | IP address actor |
| `user_agent` | TEXT | Browser/device information |
| `extra_data` | JSON | **BARU:** Storage fleksibel untuk context tambahan, metadata, atau data spesifik aplikasi |
| `created_at` | TIMESTAMP | Waktu aktivitas terjadi |

## Data Examples

### User Activity - CREATE
```json
{
    "user_id": 1,
    "actor_type": "user",
    "actor_identifier": "john@example.com",
    "actor_name": "John Doe",
    "actor_metadata": null,
    "action": "create",
    "entity": "product",
    "computed_entity": "core.Product",
    "entity_id": 123,
    "entity_name": "Laptop ASUS ROG",
    "old_values": null,
    "new_values": {
        "name": "Laptop ASUS ROG",
        "price": 15000000,
        "stock": 10
    },
    "changed_fields": null,
    "description": "Membuat produk baru: Laptop ASUS ROG",
    "ip_address": "192.168.1.1",
    "extra_data": null,
    "created_at": "2024-03-15 10:30:00"
}
```

### User Activity - UPDATE
```json
{
    "user_id": 1,
    "actor_type": "user",
    "actor_identifier": "john@example.com",
    "actor_name": "John Doe",
    "actor_metadata": null,
    "action": "update",
    "entity": "product",
    "computed_entity": "core.Product",
    "entity_id": 123,
    "entity_name": "Laptop ASUS ROG",
    "old_values": {
        "price": 15000000,
        "stock": 10
    },
    "new_values": {
        "price": 14500000,
        "stock": 8
    },
    "changed_fields": ["price", "stock"],
    "description": "Mengubah harga dari Rp 15.000.000 ke Rp 14.500.000 dan stok dari 10 ke 8",
    "ip_address": "192.168.1.1",
    "extra_data": {
        "batch_operation": false,
        "source": "admin_panel",
        "reason": "price_adjustment"
    },
    "created_at": "2024-03-15 14:20:00"
}
```

### User Activity - DELETE
```json
{
    "user_id": 1,
    "actor_type": "user",
    "actor_identifier": "john@example.com",
    "actor_name": "John Doe",
    "actor_metadata": null,
    "action": "delete",
    "entity": "product",
    "computed_entity": "core.Product",
    "entity_id": 123,
    "entity_name": "Laptop ASUS ROG",
    "old_values": {
        "name": "Laptop ASUS ROG",
        "price": 14500000,
        "stock": 8
    },
    "new_values": null,
    "changed_fields": null,
    "description": "Menghapus produk: Laptop ASUS ROG",
    "ip_address": "192.168.1.1",
    "extra_data": {
        "reason": "discontinued",
        "approved_by": "manager_id_123"
    },
    "created_at": "2024-03-15 16:45:00"
}
```

### Guest Activity - Dengan Email & Phone
```json
{
    "user_id": null,
    "actor_type": "guest",
    "actor_identifier": "guest@example.com",
    "actor_name": "Jane Smith",
    "actor_metadata": {
        "email": "guest@example.com",
        "phone": "+6281234567890",
        "source": "landing_page",
        "session_id": "sess_abc123xyz"
    },
    "action": "create",
    "entity": "contactmessage",
    "computed_entity": "core.ContactMessage",
    "entity_id": 456,
    "entity_name": "Contact Form Submission",
    "new_values": {
        "name": "Jane Smith",
        "email": "guest@example.com",
        "message": "Interested in your product"
    },
    "description": "Mengisi form kontak",
    "ip_address": "203.0.113.50",
    "extra_data": {
        "form_version": "v2.1",
        "referrer_campaign": "google_ads_campaign_123",
        "utm_source": "google"
    },
    "created_at": "2024-03-15 11:00:00"
}
```

### Guest Activity - Anonymous (Session Only)
```json
{
    "user_id": null,
    "actor_type": "guest",
    "actor_identifier": "sess_xyz789abc",
    "actor_name": "Anonymous Guest",
    "actor_metadata": {
        "session_id": "sess_xyz789abc",
        "device": "mobile",
        "browser": "Chrome"
    },
    "action": "view",
    "entity": "product",
    "computed_entity": "core.Product",
    "entity_id": 123,
    "entity_name": "Laptop ASUS ROG",
    "description": "Melihat detail produk",
    "ip_address": "203.0.113.100",
    "created_at": "2024-03-15 12:15:00"
}
```

### Guest Activity - Fallback to IP
```json
{
    "user_id": null,
    "actor_type": "guest",
    "actor_identifier": "203.0.113.200",
    "actor_name": null,
    "actor_metadata": {
        "session_id": null,
        "referrer": "https://google.com"
    },
    "action": "create",
    "entity": "cartitem",
    "computed_entity": "orders.CartItem",
    "entity_id": 789,
    "entity_name": "Add to Cart",
    "new_values": {
        "product_id": 123,
        "quantity": 2
    },
    "description": "Menambahkan produk ke keranjang",
    "ip_address": "203.0.113.200",
    "created_at": "2024-03-15 13:30:00"
}
```

## Common Queries

### Get All Activity (User + Guest)
```sql
SELECT
    al.*,
    CASE
        WHEN al.actor_type = 'user' THEN u.name
        ELSE al.actor_name
    END as display_name,
    CASE
        WHEN al.actor_type = 'user' THEN u.email
        ELSE al.actor_identifier
    END as display_identifier
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 50;
```

### Get User Activity Only
```sql
SELECT
    al.*,
    u.name as user_name,
    u.email as user_email,
    u.avatar as user_avatar
FROM activity_logs al
INNER JOIN users u ON al.user_id = u.id
WHERE al.actor_type = 'user'
  AND al.user_id = ?
ORDER BY al.created_at DESC;
```

### Get Guest Activity Only
```sql
SELECT *
FROM activity_logs
WHERE actor_type = 'guest'
ORDER BY created_at DESC
LIMIT 50;
```

### Track Guest by Identifier
```sql
SELECT *
FROM activity_logs
WHERE actor_type = 'guest'
  AND actor_identifier = ?
ORDER BY created_at DESC;
```

### Get Activity by Entity
```sql
SELECT
    al.*,
    CASE
        WHEN al.actor_type = 'user' THEN u.name
        ELSE al.actor_name
    END as actor_display_name
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.entity_type = ?
  AND al.entity_id = ?
ORDER BY al.created_at DESC;
```

### Get Recent Deletions
```sql
SELECT
    al.*,
    CASE
        WHEN al.actor_type = 'user' THEN u.name
        ELSE al.actor_name
    END as actor_display_name
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.action = 'delete'
  AND al.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY al.created_at DESC;
```

### Filter by Date Range & Actor Type
```sql
SELECT
    al.*,
    CASE
        WHEN al.actor_type = 'user' THEN u.name
        ELSE al.actor_name
    END as actor_display_name
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.created_at BETWEEN ? AND ?
  AND al.actor_type = ?
ORDER BY al.created_at DESC;
```

## Implementation Guidelines

### 1. Enums and Base Classes

```python
# core/enums/actor_type.py
from django.db import models

class ActorType(models.TextChoices):
    USER = "user", "User"
    GUEST = "guest", "Guest"

# core/enums/action_type.py
class ActionType(models.TextChoices):
    # Core CRUD operations
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    VIEW = "view", "View"

    # Authentication actions
    LOGIN = "login", "Login"
    LOGOUT = "logout", "Logout"

    # File operations
    UPLOAD = "upload", "Upload"
    DOWNLOAD = "download", "Download"

    # Status changes
    ACTIVATE = "activate", "Activate"
    DEACTIVATE = "deactivate", "Deactivate"
    PUBLISH = "publish", "Publish"
    UNPUBLISH = "unpublish", "Unpublish"

    # And more...

# core/models/_base.py
class BaseModel(models.Model):
    """Abstract base model with activity logging integration."""

    @property
    def _entity(self) -> str:
        """Simple entity type: 'product', 'user', etc."""
        return self.__class__.__name__.lower()

    @property
    def _computed_entity(self) -> str:
        """Full model path: 'core.Product', 'auth.User'."""
        return f"{self._meta.app_label}.{self.__class__.__name__}"

    class Meta:
        abstract = True
```

### 2. Django Model

```python
# models.py
from __future__ import annotations
from typing import Optional, Type
from django.db import models
from core.models._base import BaseModel
from core.enums import ActorType, ActionType
from .user import User

class ActivityLog(BaseModel):
    """
    Optimized model for comprehensive activity logging.

    Features:
    - Type-safe enums for actions and actor types
    - Direct model access via computed_entity field
    - Automatic entity type detection from BaseModel
    - Helper methods for retrieving original instances
    """

    # Actor Information
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs',
        db_index=True
    )
    actor_type = models.CharField(
        max_length=5,
        choices=ActorType.choices,
        default=ActorType.USER,
        db_index=True
    )
    actor_identifier = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    actor_name = models.CharField(max_length=255, null=True, blank=True)
    actor_metadata = models.JSONField(null=True, blank=True)

    # Activity Information
    action = models.CharField(
        max_length=12,
        choices=ActionType.choices,
        db_index=True
    )
    entity = models.CharField(max_length=50, db_index=True)  # Simple entity type
    computed_entity = models.CharField(max_length=100, db_index=True)  # Full model path
    entity_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    entity_name = models.CharField(max_length=255, null=True, blank=True)

    # Change Details
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    changed_fields = models.JSONField(null=True, blank=True)

    # Metadata
    description = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Flexible storage for additional context, metadata, or application-specific data"
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']
        # MySQL-safe indexes (avoid FK constraint conflicts)
        indexes = [
            models.Index(fields=['-created_at'], name='idx_actlog_created_at'),
            models.Index(fields=['actor_type', '-created_at'], name='idx_actlog_type_time'),
            models.Index(fields=['entity', 'entity_id'], name='idx_actlog_entity'),
            models.Index(fields=['computed_entity', 'entity_id'], name='idx_actlog_comp_ent'),
            models.Index(fields=['action', '-created_at'], name='idx_actlog_action_time'),
            models.Index(fields=['actor_identifier'], name='idx_actlog_actor_id'),
            models.Index(fields=['entity', '-created_at'], name='idx_actlog_ent_time'),
        ]

    def __str__(self) -> str:
        actor_name = self.get_actor_display_name()
        return f"{actor_name} {self.action} {self.entity}"

    def get_actor_display_name(self) -> str:
        """Get display name for the activity actor."""
        if self.actor_type == ActorType.USER and self.user:
            return getattr(self.user, 'name', None) or self.user.username
        return self.actor_name or 'Anonymous'

    def get_target_instance(self) -> Optional[models.Model]:
        """
        Retrieve the original target instance using computed_entity path.

        Example:
            activity_log = ActivityLog.objects.get(id=1)
            original_product = activity_log.get_target_instance()
        """
        if not self.computed_entity or not self.entity_id:
            return None
        try:
            from django.apps import apps
            app_label, model_name = self.computed_entity.split('.')
            model_class = apps.get_model(app_label, model_name)
            return model_class.objects.get(pk=self.entity_id)
        except (ValueError, LookupError, model_class.DoesNotExist):
            return None

    def get_target_model_class(self) -> Optional[Type[models.Model]]:
        """
        Get the model class for the target entity.

        Example:
            ProductModel = activity_log.get_target_model_class()
            # Use: ProductModel.objects.filter(...)
        """
        if not self.computed_entity:
            return None
        try:
            from django.apps import apps
            app_label, model_name = self.computed_entity.split('.')
            return apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            return None

    def get_extra_value(self, key: str, default=None):
        """Safely retrieve value from extra_data JSON field."""
        if not self.extra_data or not isinstance(self.extra_data, dict):
            return default
        return self.extra_data.get(key, default)

    def set_extra_value(self, key: str, value) -> None:
        """Safely set value in extra_data JSON field."""
        if not isinstance(self.extra_data, dict):
            self.extra_data = {}
        self.extra_data[key] = value

    @classmethod
    def create_for_instance(cls, instance: BaseModel, action: str, **kwargs) -> 'ActivityLog':
        """
        Helper method with automatic entity type detection.

        Example:
            ActivityLog.create_for_instance(
                instance=product_instance,
                action=ActionType.CREATE,
                user=request.user,
                extra_data={'integration_source': 'shopify', 'batch_id': 'batch_123'}
            )
        """
        return cls.objects.create(
            action=action,
            entity=instance._entity,  # Automatic detection
            computed_entity=instance._computed_entity,  # Full path
            entity_id=instance.pk,
            entity_name=str(instance),
            **kwargs
        )
```

### 2. Helper Function for Logging

```python
# utils/activity_logger.py
import json
from django.contrib.auth import get_user_model
from .models import ActivityLog

User = get_user_model()

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_activity(request, action, entity_type, entity_id=None, entity_name=None,
                old_values=None, new_values=None, changed_fields=None,
                description=None, guest_name=None, guest_email=None,
                guest_phone=None, **kwargs):
    """
    Log activity untuk user atau guest

    Args:
        request: Django request object
        action: str - 'create', 'update', 'delete', 'view', dll
        entity_type: str - 'product', 'order', 'customer', dll
        entity_id: int - ID dari entity
        entity_name: str - Nama entity untuk display
        old_values: dict - Data sebelum perubahan
        new_values: dict - Data setelah perubahan
        changed_fields: list - List field yang berubah
        description: str - Deskripsi human-readable
        guest_name: str - Nama guest (optional)
        guest_email: str - Email guest (optional)
        guest_phone: str - Phone guest (optional)
        **kwargs: Additional metadata untuk guest
    """
    log_data = {
        'action': action,
        'entity_type': entity_type,
        'entity_id': entity_id,
        'entity_name': entity_name,
        'old_values': old_values,
        'new_values': new_values,
        'changed_fields': changed_fields,
        'description': description,
        'ip_address': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
    }

    # Authenticated User
    if request.user.is_authenticated:
        log_data['user'] = request.user
        log_data['actor_type'] = 'user'
        log_data['actor_identifier'] = request.user.email
        log_data['actor_name'] = request.user.get_full_name() or request.user.username
        log_data['actor_metadata'] = None

    # Guest
    else:
        log_data['user'] = None
        log_data['actor_type'] = 'guest'

        # Prioritas identifier: email > phone > session > IP
        log_data['actor_identifier'] = (
            guest_email or
            guest_phone or
            request.session.session_key or
            get_client_ip(request)
        )

        log_data['actor_name'] = guest_name or 'Anonymous Guest'

        # Build metadata
        metadata = {
            'email': guest_email,
            'phone': guest_phone,
            'session_id': request.session.session_key,
            'device': kwargs.get('device'),
            'browser': kwargs.get('browser'),
            'source': kwargs.get('source'),
            'referrer': request.META.get('HTTP_REFERER'),
        }

        # Filter out None values
        log_data['actor_metadata'] = {k: v for k, v in metadata.items() if v is not None}

    # Create log
    ActivityLog.objects.create(**log_data)

def log_model_change(request, instance, action, old_instance=None):
    """
    Helper untuk log perubahan model Django

    Args:
        request: Django request object
        instance: Model instance yang diubah
        action: 'create', 'update', atau 'delete'
        old_instance: Model instance sebelum perubahan (untuk update)
    """
    entity_type = instance.__class__.__name__.lower()
    entity_name = str(instance)

    if action == 'create':
        log_activity(
            request=request,
            action=action,
            entity_type=entity_type,
            entity_id=instance.pk,
            entity_name=entity_name,
            new_values=instance.__dict__,
            description=f"Membuat {entity_type} baru: {entity_name}"
        )

    elif action == 'update' and old_instance:
        # Detect changed fields
        changed_fields = []
        old_values = {}
        new_values = {}

        for field in instance._meta.fields:
            field_name = field.name
            if field_name in ['id', 'created_at', 'updated_at']:
                continue

            old_val = getattr(old_instance, field_name)
            new_val = getattr(instance, field_name)

            if old_val != new_val:
                changed_fields.append(field_name)
                old_values[field_name] = old_val
                new_values[field_name] = new_val

        if changed_fields:
            log_activity(
                request=request,
                action=action,
                entity_type=entity_type,
                entity_id=instance.pk,
                entity_name=entity_name,
                old_values=old_values,
                new_values=new_values,
                changed_fields=changed_fields,
                description=f"Mengubah {entity_type}: {entity_name}"
            )

    elif action == 'delete':
        log_activity(
            request=request,
            action=action,
            entity_type=entity_type,
            entity_id=instance.pk,
            entity_name=entity_name,
            old_values=instance.__dict__,
            description=f"Menghapus {entity_type}: {entity_name}"
        )
```

### 3. Usage Examples

```python
# views.py
from django.shortcuts import render, redirect
from .models import Product
from .utils.activity_logger import log_activity, log_model_change

# Example 1: User membuat produk
def create_product(request):
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            stock=request.POST['stock']
        )

        # Log activity
        log_model_change(request, product, 'create')

        return redirect('product_detail', pk=product.pk)

    return render(request, 'product_form.html')

# Example 2: User update produk
def update_product(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        # Simpan state lama
        old_product = Product.objects.get(pk=pk)

        # Update
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.save()

        # Log activity
        log_model_change(request, product, 'update', old_product)

        return redirect('product_detail', pk=product.pk)

    return render(request, 'product_form.html', {'product': product})

# Example 3: Guest mengisi form kontak
def contact_form(request):
    if request.method == 'POST':
        contact = ContactForm.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            message=request.POST['message']
        )

        # Log guest activity
        log_activity(
            request=request,
            action='create',
            entity_type='contact_form',
            entity_id=contact.pk,
            entity_name='Contact Form Submission',
            new_values={
                'name': contact.name,
                'email': contact.email,
                'message': contact.message
            },
            description=f"Guest mengisi form kontak",
            guest_name=contact.name,
            guest_email=contact.email,
            guest_phone=contact.phone,
            source='contact_page'
        )

        return redirect('contact_success')

    return render(request, 'contact_form.html')

# Example 4: Guest anonymous melihat produk
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)

    # Log view activity (termasuk guest)
    log_activity(
        request=request,
        action='view',
        entity_type='product',
        entity_id=product.pk,
        entity_name=product.name,
        description=f"Melihat detail produk: {product.name}"
    )

    return render(request, 'product_detail.html', {'product': product})
```

### 4. Enhanced Usage Examples (New Features)

```python
# Example 1: Using create_for_instance (Recommended)
def create_product(request):
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            stock=request.POST['stock']
        )

        # Automatic entity detection and logging
        ActivityLog.create_for_instance(
            instance=product,
            action=ActionType.CREATE,
            user=request.user,
            description=f"Created product: {product.name}",
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )

        return redirect('product_detail', pk=product.pk)

# Example 2: Retrieving original instances from logs
def activity_details(request, log_id):
    activity_log = ActivityLog.objects.get(id=log_id)

    # Get original instance directly!
    original_instance = activity_log.get_target_instance()
    if original_instance:
        print(f"Found original: {original_instance}")
        # Can access all fields: original_instance.name, original_instance.price, etc.

    # Or get model class for queries
    ModelClass = activity_log.get_target_model_class()
    if ModelClass:
        related_items = ModelClass.objects.filter(category="electronics")

# Example 3: Query patterns with computed_entity
# Find all activities on Product models
product_activities = ActivityLog.objects.filter(
    computed_entity="core.Product"
).order_by('-created_at')

# Find activities on specific product instance
specific_product_activities = ActivityLog.objects.filter(
    computed_entity="core.Product",
    entity_id=123
)

# Bulk retrieve original instances
activity_logs = ActivityLog.objects.filter(action=ActionType.DELETE)
for log in activity_logs:
    # This is now super efficient - no conditional imports!
    if original := log.get_target_instance():
        print(f"Deleted item was: {original}")
```

### 5. Middleware for Auto-Logging (Optional)

```python
# middleware/activity_logging.py
from django.utils.deprecation import MiddlewareMixin
from ..utils.activity_logger import log_activity

class ActivityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware untuk auto-log certain actions
    Contoh: auto-log setiap POST request
    """

    def process_response(self, request, response):
        # Skip untuk admin panel, static files, dll
        if any([
            request.path.startswith('/admin/'),
            request.path.startswith('/static/'),
            request.path.startswith('/media/'),
        ]):
            return response

        # Auto-log successful POST requests
        if request.method == 'POST' and 200 <= response.status_code < 300:
            # Implement your auto-logging logic here
            pass

        return response
```

### 3. Logging Best Practices
- Log setelah operasi berhasil (setelah commit transaction)
- Gunakan queue/background job untuk logging agar tidak memperlambat response
- Sanitize data sensitif (password, token, credit card, dll) sebelum disimpan
- Batasi ukuran `old_values` dan `new_values` untuk data besar
- Untuk guest, simpan identifier yang paling reliable (email > phone > session > IP)

### 4. UI Display Recommendations

#### Display Actor Information
```php
// Blade template example
@if($log->actor_type === 'user' && $log->user)
    <div class="flex items-center">
        <img src="{{ $log->user->avatar }}" class="w-8 h-8 rounded-full">
        <span class="ml-2">{{ $log->user->name }}</span>
    </div>
@else
    <div class="flex items-center">
        <div class="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
            <i class="icon-guest"></i>
        </div>
        <span class="ml-2">{{ $log->actor_name ?? 'Guest' }}</span>
        <span class="ml-1 text-sm text-gray-500">
            ({{ $log->actor_identifier }})
        </span>
    </div>
@endif
```

#### Group Activities
- Group by date: "Hari ini", "Kemarin", "Minggu ini"
- Highlight changed fields dengan warna berbeda
- Format timestamp: "2 jam yang lalu", "15 Mar 2024, 10:30"
- Show badge untuk actor type: "User" atau "Guest"

#### Pagination
- Gunakan pagination untuk performa
- Default 50 items per page
- Infinite scroll untuk mobile

### 5. Performance Considerations
- Gunakan pagination (LIMIT + OFFSET) atau cursor-based pagination
- Index sudah dibuat pada kolom yang sering di-query
- Pertimbangkan archiving untuk log lama (> 1 tahun)
- Gunakan database read replica untuk query activity log
- Cache count queries untuk dashboard statistics

### 6. Security & Privacy

#### Data Sensitif
- Hindari menyimpan password, token, credit card di `old_values`/`new_values`
- Hash/encrypt data sensitif jika perlu disimpan
- Mask partial data: "email: j***n@example.com", "phone: +628****7890"

#### Access Control
- User hanya bisa lihat log mereka sendiri
- Admin/Manager bisa lihat semua log
- Guest tracking harus comply dengan privacy policy
- Implement GDPR right to be forgotten untuk guest data

#### Guest Privacy
- Inform user tentang tracking di privacy policy
- Berikan opsi opt-out untuk guest tracking
- Auto-delete guest log setelah periode tertentu (misal: 90 hari)
- Anonymize guest data jika perlu

## Design Benefits

### Original Features
✅ **Flexible Actor Support**: Mendukung user dan guest dengan struktur yang sama
✅ **General Guest Handling**: `actor_metadata` JSON bisa simpan data apapun
✅ **Backward Compatible**: User tetap relasi ke tabel users
✅ **Fallback Mechanism**: Bisa pakai IP/session jika guest tanpa identitas
✅ **Easy Querying**: Filter by actor_type dengan mudah
✅ **UI Friendly**: Field `description` dan `entity_name` siap display

### Enhanced Features (NEW)
✅ **Type-Safe Enums**: ActionType dan ActorType mencegah typos dan inconsistency
✅ **Direct Model Access**: Field `computed_entity` memungkinkan akses langsung ke model asli
✅ **Automatic Detection**: BaseModel integration untuk deteksi otomatis entity type
✅ **Zero Conditional Imports**: Tidak perlu lagi if/else untuk import model yang berbeda
✅ **MySQL-Safe Indexes**: Optimized indexes yang tidak konflik dengan foreign key constraints
✅ **Flexible Extra Data**: JSON field untuk context tambahan dengan helper methods
✅ **Developer Friendly**: Helper methods `get_target_instance()`, `get_extra_value()`, dan `create_for_instance()`
✅ **Maintainable Code**: Reduced boilerplate dengan automatic entity detection
✅ **Future Proof**: Extensible design dengan extra_data untuk kebutuhan yang berkembang

### Performance Improvements
- **Optimized Field Sizes**: `actor_type` (5 chars), `action` (12 chars)
- **MySQL-Safe Indexes**: Strategic combinations yang menghindari FK constraint conflicts
- **Direct Model Access**: Eliminates need for complex conditional logic
- **Efficient Queries**: Better index utilization untuk reporting dan analytics
- **JSON Storage**: Optimized storage untuk metadata dan extra data
- **Rollback Safe**: Migration-friendly design untuk development dan production

## Additional Notes

### User Deletion Handling
Desain ini menggunakan `ON DELETE SET NULL`, artinya jika user dihapus, `user_id` di activity log akan menjadi NULL tapi record tetap ada dengan data `actor_name` dan `actor_identifier`.

**Rekomendasi**: Tetap implementasikan soft delete di tabel users untuk menghindari kehilangan konteks:
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;
```

### Guest Identifier Priority
Saat logging guest activity, gunakan prioritas berikut untuk `actor_identifier`:
1. **Email** (paling reliable jika tersedia)
2. **Phone** (reliable kedua)
3. **Session ID** (untuk tracking dalam session)
4. **IP Address** (fallback terakhir)

### Actor Metadata Examples
```json
// Guest dengan identitas lengkap
{
    "email": "guest@example.com",
    "phone": "+6281234567890",
    "session_id": "sess_abc123",
    "source": "landing_page",
    "device": "mobile",
    "browser": "Chrome 120",
    "referrer": "https://google.com"
}

// Guest anonymous
{
    "session_id": "sess_xyz789",
    "device": "desktop",
    "browser": "Firefox 121",
    "referrer": null
}
```

### Extra Data Usage Examples

#### E-commerce Integration Tracking
```python
ActivityLog.create_for_instance(
    instance=product,
    action=ActionType.UPDATE,
    user=request.user,
    extra_data={
        'integration_source': 'shopify',
        'sync_batch_id': 'batch_12345',
        'processing_time': 2.5,
        'external_id': 'shop_prod_789'
    }
)
```

#### API Integration & Performance Monitoring
```python
log = ActivityLog.objects.create(
    action=ActionType.CREATE,
    entity='order',
    extra_data={
        'api_version': 'v2.1',
        'client_app': 'mobile_app_ios',
        'request_id': 'req_abc123',
        'performance_metrics': {
            'query_count': 5,
            'cache_hits': 12,
            'response_time': 120
        }
    }
)
```

#### Batch Operations & Error Tracking
```python
extra_data = {
    'batch_operation': True,
    'total_records': 150,
    'success_count': 148,
    'error_count': 2,
    'error_records': [{'id': 123, 'error': 'validation_failed'}],
    'retry_attempts': 2
}
```

#### Dynamic Usage with Helper Methods
```python
# Retrieve values safely
log = ActivityLog.objects.get(id=1)
batch_id = log.get_extra_value('sync_batch_id')
processing_time = log.get_extra_value('processing_time', 0.0)

# Set values dynamically
log.set_extra_value('completion_status', 'success')
log.set_extra_value('retry_count', 2)
log.save()
```

### Future Enhancements
- Tambah field `changes_summary` untuk summary perubahan dalam 1 kalimat
- Tambah `tags` JSON untuk kategorisasi custom
- Tambah `related_entity_type` dan `related_entity_id` untuk relasi antar entitas
- Implementasi retention policy dengan auto-delete berdasarkan actor_type:
  - User logs: retain 2 tahun
  - Guest logs: retain 90 hari
- Dashboard analytics: guest conversion tracking, activity heatmap
- Export functionality untuk compliance (GDPR data export)