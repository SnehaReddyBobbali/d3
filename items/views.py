from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import LostItem, Claim
from .forms import LostItemForm, ClaimForm


def home(request):
    """Home page with list of all lost items"""
    items = LostItem.objects.all()
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        items = items.filter(status=status)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_lost__icontains=search_query)
        )
    
    context = {
        'items': items,
        'categories': LostItem.CATEGORY_CHOICES,
        'statuses': LostItem.STATUS_CHOICES,
    }
    return render(request, 'items/home.html', context)


def item_detail(request, pk):
    """Detail page for a specific lost item"""
    item = get_object_or_404(LostItem, pk=pk)
    claims = item.claims.all() if request.user.is_authenticated else []
    
    # Check if current user has already claimed this item
    user_has_claimed = False
    if request.user.is_authenticated:
        user_has_claimed = item.claims.filter(claimed_by=request.user).exists()
    
    context = {
        'item': item,
        'claims': claims,
        'user_has_claimed': user_has_claimed,
    }
    return render(request, 'items/item_detail.html', context)


@login_required
def post_item(request):
    """View for posting a new lost item"""
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            messages.success(request, 'Item posted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = LostItemForm()
    
    return render(request, 'items/post_item.html', {'form': form})


@login_required
def edit_item(request, pk):
    """View for editing an existing lost item"""
    item = get_object_or_404(LostItem, pk=pk)
    
    # Only the user who posted can edit
    if item.posted_by != request.user:
        messages.error(request, 'You can only edit items you posted.')
        return redirect('item_detail', pk=pk)
    
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_detail', pk=pk)
    else:
        form = LostItemForm(instance=item)
    
    return render(request, 'items/edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, pk):
    """View for deleting a lost item"""
    item = get_object_or_404(LostItem, pk=pk)
    
    # Only the user who posted can delete
    if item.posted_by != request.user:
        messages.error(request, 'You can only delete items you posted.')
        return redirect('item_detail', pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('home')
    
    return render(request, 'items/delete_item.html', {'item': item})


@login_required
def my_items(request):
    """View for displaying user's posted items"""
    items = LostItem.objects.filter(posted_by=request.user)
    return render(request, 'items/my_items.html', {'items': items})


@login_required
def claim_item(request, pk):
    """View for claiming a lost item"""
    item = get_object_or_404(LostItem, pk=pk)
    
    # Check if user already claimed this item
    if item.claims.filter(claimed_by=request.user).exists():
        messages.warning(request, 'You have already claimed this item.')
        return redirect('item_detail', pk=pk)
    
    # User cannot claim their own item
    if item.posted_by == request.user:
        messages.error(request, 'You cannot claim your own item.')
        return redirect('item_detail', pk=pk)
    
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimed_by = request.user
            claim.save()
            messages.success(request, 'Claim submitted successfully!')
            return redirect('item_detail', pk=pk)
    else:
        form = ClaimForm()
    
    return render(request, 'items/claim_item.html', {'form': form, 'item': item})


@login_required
def my_claims(request):
    """View for displaying user's claims"""
    claims = Claim.objects.filter(claimed_by=request.user)
    return render(request, 'items/my_claims.html', {'claims': claims})


@login_required
def manage_claims(request, pk):
    """View for item owner to manage claims on their items"""
    item = get_object_or_404(LostItem, pk=pk)
    
    # Only the item owner can manage claims
    if item.posted_by != request.user:
        messages.error(request, 'You can only manage claims on your own items.')
        return redirect('item_detail', pk=pk)
    
    claims = item.claims.all()
    return render(request, 'items/manage_claims.html', {'item': item, 'claims': claims})


@login_required
def update_claim_status(request, claim_pk, status):
    """View for updating claim status"""
    claim = get_object_or_404(Claim, pk=claim_pk)
    
    # Only the item owner can update claim status
    if claim.item.posted_by != request.user:
        messages.error(request, 'You do not have permission to update this claim.')
        return redirect('item_detail', pk=claim.item.pk)
    
    if status in ['approved', 'rejected']:
        claim.status = status
        claim.save()
        
        # If approved, mark item as claimed
        if status == 'approved':
            claim.item.status = 'claimed'
            claim.item.save()
            messages.success(request, f'Claim approved! Item marked as claimed.')
        else:
            messages.success(request, 'Claim rejected.')
    
    return redirect('manage_claims', pk=claim.item.pk)
