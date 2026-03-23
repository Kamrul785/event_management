from django.contrib import messages
from django.shortcuts import redirect, render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not all([name, email, subject, message_text]):
            messages.error(request, 'Please fill out all contact form fields.')
            return render(
                request,
                'contact.html',
                {'form_data': request.POST},
            )

        messages.success(request, 'Thanks for your message. We will contact you within one business day.')
        return redirect('contact')

    return render(request, 'contact.html')


def help_center(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Help Center',
            'page_heading': 'Help Center',
            'page_intro': 'Get quick answers and guidance for using Eventzilla effectively.',
            'content_items': [
                'How to create and publish events',
                'Managing participants and registrations',
                'Roles, permissions, and team workflows',
                'Common troubleshooting and support options',
            ],
        },
    )


def api_documentation(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'API Documentation',
            'page_heading': 'API Documentation',
            'page_intro': 'Technical references for integrating Eventzilla with your workflows.',
            'content_items': [
                'Authentication and token usage',
                'Events and participant endpoints overview',
                'Request and response format basics',
                'Best practices for secure integrations',
            ],
        },
    )


def event_planning_guide(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Event Planning Guide',
            'page_heading': 'Event Planning Guide',
            'page_intro': 'A practical checklist to plan, launch, and run successful events.',
            'content_items': [
                'Define goals, audience, and success metrics',
                'Prepare timelines, logistics, and communication',
                'Promote the event and manage registrations',
                'Track outcomes and improve future events',
            ],
        },
    )


def best_practices(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Best Practices',
            'page_heading': 'Best Practices',
            'page_intro': 'Recommended patterns for reliable event operations and participant experience.',
            'content_items': [
                'Use clear event titles and concise descriptions',
                'Keep schedules and participant lists updated',
                'Set proper access levels for team members',
                'Review post-event analytics and feedback regularly',
            ],
        },
    )


def video_tutorials(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Video Tutorials',
            'page_heading': 'Video Tutorials',
            'page_intro': 'Step-by-step walkthrough topics to help you master Eventzilla features.',
            'content_items': [
                'Getting started and dashboard overview',
                'Creating, editing, and publishing events',
                'Working with categories and participants',
                'Admin controls and reporting essentials',
            ],
        },
    )


def privacy_policy(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Privacy Policy',
            'page_heading': 'Privacy Policy',
            'page_intro': 'How Eventzilla handles, stores, and protects personal information.',
            'content_items': [
                'Information we collect and why',
                'How data is used to provide services',
                'User rights and account controls',
                'Security practices and retention approach',
            ],
        },
    )


def terms_of_service(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Terms of Service',
            'page_heading': 'Terms of Service',
            'page_intro': 'The core terms governing use of the Eventzilla platform.',
            'content_items': [
                'Account responsibilities and permitted use',
                'Content ownership and user obligations',
                'Service availability and limitation clauses',
                'Contact channels for legal questions',
            ],
        },
    )


def cookie_policy(request):
    return render(
        request,
        'content_page.html',
        {
            'page_title': 'Cookie Policy',
            'page_heading': 'Cookie Policy',
            'page_intro': 'How cookies are used to improve platform functionality and analytics.',
            'content_items': [
                'Essential cookies required for login sessions',
                'Analytics cookies for performance insights',
                'Preference cookies for better user experience',
                'Controls for managing cookie behavior',
            ],
        },
    )


def no_permission(request):
    return render(request, 'no_permission.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)