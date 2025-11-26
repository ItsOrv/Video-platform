// Video Preview on Hover functionality
class VideoPreview {
    constructor() {
        this.previewContainer = null;
        this.currentVideo = null;
        this.previewTimeout = null;
        this.init();
    }

    init() {
        // Create preview container
        this.createPreviewContainer();
        
        // Attach event listeners to all video cards
        document.querySelectorAll('.video-card').forEach(card => {
            this.attachPreviewEvents(card);
        });
    }

    createPreviewContainer() {
        this.previewContainer = document.createElement('div');
        this.previewContainer.id = 'videoPreview';
        this.previewContainer.className = 'fixed z-50 pointer-events-none opacity-0 transition-opacity duration-300';
        this.previewContainer.innerHTML = `
            <div class="glass-effect rounded-2xl overflow-hidden shadow-2xl" style="width: 320px;">
                <div class="relative aspect-video bg-black">
                    <video class="w-full h-full object-cover" muted preload="metadata"></video>
                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent p-4 flex flex-col justify-end">
                        <h4 class="text-sm font-bold mb-1 line-clamp-2"></h4>
                        <div class="flex items-center justify-between text-xs text-gray-400">
                            <span class="views-count"></span>
                            <span class="duration"></span>
                        </div>
                    </div>
                </div>
                <div class="p-3 bg-white/5">
                    <p class="text-xs text-gray-300 line-clamp-2 description"></p>
                    <div class="flex items-center justify-between mt-2">
                        <span class="text-xs text-gray-400 uploader"></span>
                        <span class="text-xs text-gray-400 date"></span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.previewContainer);
    }

    attachPreviewEvents(card) {
        const videoId = card.dataset.videoId || card.dataset.videoSrc;
        if (!videoId) return;

        card.addEventListener('mouseenter', (e) => {
            this.showPreview(card, e);
        });

        card.addEventListener('mouseleave', () => {
            this.hidePreview();
        });

        card.addEventListener('mousemove', (e) => {
            this.updatePreviewPosition(e);
        });
    }

    showPreview(card, event) {
        clearTimeout(this.previewTimeout);
        
        this.previewTimeout = setTimeout(() => {
            const videoSrc = card.dataset.videoSrc;
            const videoId = card.dataset.videoId;
            const title = card.querySelector('h3')?.textContent || '';
            const description = card.querySelector('p')?.textContent || '';
            const thumbnail = card.querySelector('img')?.src || '';
            
            if (!videoSrc && !videoId) return;

            // Update preview content
            const video = this.previewContainer.querySelector('video');
            const titleEl = this.previewContainer.querySelector('h4');
            const descEl = this.previewContainer.querySelector('.description');
            const viewsEl = this.previewContainer.querySelector('.views-count');
            const durationEl = this.previewContainer.querySelector('.duration');
            const uploaderEl = this.previewContainer.querySelector('.uploader');
            const dateEl = this.previewContainer.querySelector('.date');

            if (videoSrc) {
                video.src = videoSrc;
                video.currentTime = 5; // Start at 5 seconds
                video.play().catch(() => {}); // Muted autoplay
            } else {
                video.poster = thumbnail;
            }

            titleEl.textContent = title;
            descEl.textContent = description;
            
            // Get additional data if available
            const views = card.dataset.views || '0';
            const duration = card.dataset.duration || '';
            const uploader = card.dataset.uploader || '';
            const date = card.dataset.date || '';

            viewsEl.textContent = `${views} views`;
            if (duration) {
                durationEl.textContent = this.formatDuration(duration);
            }
            uploaderEl.textContent = uploader;
            dateEl.textContent = date;

            // Show preview
            this.previewContainer.classList.remove('opacity-0');
            this.previewContainer.classList.add('opacity-100');
            this.updatePreviewPosition(event);
        }, 500); // Delay before showing preview
    }

    hidePreview() {
        clearTimeout(this.previewTimeout);
        
        const video = this.previewContainer.querySelector('video');
        if (video) {
            video.pause();
            video.currentTime = 0;
        }

        this.previewContainer.classList.remove('opacity-100');
        this.previewContainer.classList.add('opacity-0');
    }

    updatePreviewPosition(event) {
        if (!this.previewContainer.classList.contains('opacity-100')) return;

        const rect = this.previewContainer.getBoundingClientRect();
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        let left = event.clientX + 20;
        let top = event.clientY + 20;

        // Adjust if preview goes off screen
        if (left + rect.width > windowWidth) {
            left = event.clientX - rect.width - 20;
        }
        if (top + rect.height > windowHeight) {
            top = event.clientY - rect.height - 20;
        }

        this.previewContainer.style.left = `${left}px`;
        this.previewContainer.style.top = `${top}px`;
    }

    formatDuration(seconds) {
        if (!seconds) return '';
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new VideoPreview();
    });
} else {
    new VideoPreview();
}

