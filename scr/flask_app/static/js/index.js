// Dashboard Animations and Interactions
document.addEventListener('DOMContentLoaded', function () {
    // Initialize animations for stats cards
    const statsCards = document.querySelectorAll('.stats-card');
    statsCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add hover animations to stats icons
    const statsIcons = document.querySelectorAll('.stats-icon i');
    statsIcons.forEach(icon => {
        icon.addEventListener('mouseover', function () {
            this.classList.add('fa-beat');
        });

        icon.addEventListener('mouseout', function () {
            this.classList.remove('fa-beat');
        });
    });

    // Add ripple effect to all buttons and action items
    const buttons = document.querySelectorAll('.btn, .stats-action, .quick-action-item');
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            createRippleEffect(e, this);
        });
    });

    // Animate progress bars on load
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';

        setTimeout(() => {
            bar.style.transition = 'width 1s ease';
            bar.style.width = width;
        }, 500);
    });

    // Add counter animation to stats numbers
    const statsNumbers = document.querySelectorAll('.stats-number');
    statsNumbers.forEach(number => {
        const finalValue = parseInt(number.textContent);
        if (!isNaN(finalValue)) {
            animateCounter(number, 0, finalValue, 1500);
        }
    });

    // Add counter animation to version number
    const versionElement = document.querySelector('.version-number');
    if (versionElement) {
        const version = versionElement.textContent;
        versionElement.textContent = '0.0.0';

        let currentVersion = [0, 0, 0];
        const targetVersion = version.split('.').map(num => parseInt(num));

        const interval = setInterval(() => {
            let updated = false;

            for (let i = 2; i >= 0; i--) {
                if (currentVersion[i] < targetVersion[i]) {
                    currentVersion[i]++;
                    updated = true;
                    break;
                }
            }

            versionElement.textContent = currentVersion.join('.');

            if (!updated) {
                clearInterval(interval);
            }
        }, 100);
    }

    // Add pulse animation to status badge
    const statusBadge = document.querySelector('.badge.bg-success');
    if (statusBadge) {
        setInterval(() => {
            statusBadge.classList.add('pulse-animation');
            setTimeout(() => {
                statusBadge.classList.remove('pulse-animation');
            }, 1000);
        }, 3000);
    }

    // Add refresh functionality to the refresh button
    const refreshButton = document.querySelector('#refreshActivities');
    if (refreshButton) {
        refreshButton.addEventListener('click', function () {
            // Add spinning animation to the refresh icon
            const icon = this.querySelector('i');
            icon.classList.add('fa-spin');

            // Fetch recent activities from the API - barcha aktivliklarni olish uchun limit parametrini o'zgartirdim
            fetch('/api/activities?limit=100')
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.activities) {
                        updateActivitiesTimeline(data.activities);
                    }
                    // Stop spinning animation
                    icon.classList.remove('fa-spin');
                })
                .catch(error => {
                    console.error('Error fetching activities:', error);
                    // Stop spinning animation
                    icon.classList.remove('fa-spin');
                });
        });
    }

    // Add staggered animation to timeline items
    animateTimelineItems();

    // Add staggered animation to system info items
    const infoItems = document.querySelectorAll('.system-info-item');
    infoItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';

        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 800 + (index * 100));
    });

    // Add staggered animation to quick action items
    const quickActionItems = document.querySelectorAll('.quick-action-item');
    quickActionItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(10px)';

        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 1000 + (index * 100));
    });

    // Log page view activity
    logActivity('PAGE_VIEW', 'Dashboard page viewed');
});

// Function to update the activities timeline
function updateActivitiesTimeline(activities) {
    const timelineContainer = document.getElementById('activitiesTimeline');

    // Clear existing timeline items
    timelineContainer.innerHTML = '';

    if (activities.length === 0) {
        // Show empty state
        timelineContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-history fa-3x text-muted mb-3"></i>
                <p class="text-muted">No recent activities found</p>
            </div>
        `;
        return;
    }

    // Add new timeline items
    activities.forEach(activity => {
        // Determine icon class based on activity type
        let iconClass = 'fas fa-cog';
        let bgColorClass = 'bg-secondary';
        let activityTitle = 'System Activity';

        if (activity.activity_type === 'LOGIN' || activity.activity_type === 'LOGOUT') {
            iconClass = 'fas fa-user';
            bgColorClass = 'bg-info';
            activityTitle = activity.activity_type === 'LOGIN' ? 'User Login' : 'User Logout';
        } else if (activity.activity_type === 'BOT_ADD' || activity.activity_type === 'BOT_UPDATE' || activity.activity_type === 'BOT_DELETE') {
            iconClass = 'fas fa-robot';
            bgColorClass = activity.activity_type === 'BOT_ADD' ? 'bg-primary' :
                (activity.activity_type === 'BOT_UPDATE' ? 'bg-warning' : 'bg-danger');
            activityTitle = activity.activity_type === 'BOT_ADD' ? 'New Bot Added' :
                (activity.activity_type === 'BOT_UPDATE' ? 'Bot Updated' : 'Bot Deleted');
        } else if (activity.activity_type === 'DATABASE_INIT') {
            iconClass = 'fas fa-database';
            bgColorClass = 'bg-success';
            activityTitle = 'Database Initialized';
        } else if (activity.activity_type === 'PAGE_VIEW') {
            iconClass = 'fas fa-eye';
            bgColorClass = 'bg-info';
            activityTitle = 'Page View';
        } else if (activity.activity_type === 'TOKEN_COPY') {
            iconClass = 'fas fa-copy';
            bgColorClass = 'bg-warning';
            activityTitle = 'Token Copied';
        }

        // Create timeline item with IP and user agent details
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item';
        timelineItem.style.opacity = '0';
        timelineItem.style.transform = 'translateX(-20px)';

        // Create details section for IP and user agent
        let detailsHTML = '';
        if (activity.ip_address) {
            detailsHTML += `<span><i class="fas fa-network-wired"></i> ${activity.ip_address}</span>`;
        }
        if (activity.username) {
            detailsHTML += `<span><i class="fas fa-user"></i> ${activity.username}</span>`;
        }
        if (activity.user_agent) {
            // Truncate user agent if it's too long
            const userAgent = activity.user_agent.length > 30 ?
                activity.user_agent.substring(0, 30) + '...' :
                activity.user_agent;
            detailsHTML += `<span title="${activity.user_agent}"><i class="fas fa-desktop"></i> ${userAgent}</span>`;
        }

        timelineItem.innerHTML = `
            <div class="timeline-icon ${bgColorClass}">
                <i class="${iconClass}"></i>
            </div>
            <div class="timeline-content">
                <h6 class="timeline-title">${activityTitle}</h6>
                <p class="timeline-text">${activity.description}</p>
                <div class="timeline-details">
                    ${detailsHTML}
                </div>
                <span class="timeline-time" title="${activity.timestamp}">${activity.timestamp}</span>
            </div>
        `;

        timelineContainer.appendChild(timelineItem);
    });

    // Animate the new timeline items
    animateTimelineItems();
}

// Function to animate timeline items with staggered effect
function animateTimelineItems() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';

        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 500 + (index * 100)); // Animatsiya vaqtini kamaytirib, ko'p elementlar uchun moslashtirildi
    });
}

// Function to log activity
function logActivity(activityType, description) {
    fetch('/api/activities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            activity_type: activityType,
            description: description
        })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error logging activity:', data.message);
            }
        })
        .catch(error => {
            console.error('Error logging activity:', error);
        });
}

// Helper function to create ripple effect
function createRippleEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const circle = document.createElement('span');
    const diameter = Math.max(rect.width, rect.height);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${x - radius}px`;
    circle.style.top = `${y - radius}px`;
    circle.classList.add('ripple');

    const ripple = element.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }

    element.appendChild(circle);

    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Helper function to animate counter
function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.textContent = end;
        }
    };
    window.requestAnimationFrame(step);
}