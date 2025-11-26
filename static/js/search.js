// Advanced Search functionality
class AdvancedSearch {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.suggestionsContainer = document.getElementById('searchSuggestions');
        this.resultsGrid = document.getElementById('resultsGrid');
        this.loadingState = document.getElementById('loadingState');
        this.noResults = document.getElementById('noResults');
        this.resultsCount = document.getElementById('resultsCount');
        this.searchTimeout = null;
        this.currentQuery = '';
        this.init();
    }

    init() {
        // Search input event
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearchInput(e.target.value);
        });

        // Filter change events
        document.getElementById('categoryFilter').addEventListener('change', () => this.performSearch());
        document.getElementById('durationFilter').addEventListener('change', () => this.performSearch());
        document.getElementById('dateFilter').addEventListener('change', () => this.performSearch());
        document.getElementById('premiumFilter').addEventListener('change', () => this.performSearch());
        document.getElementById('freeFilter').addEventListener('change', () => this.performSearch());
        document.getElementById('sortFilter').addEventListener('change', () => this.performSearch());

        // Clear filters
        document.getElementById('clearFilters').addEventListener('click', () => this.clearFilters());

        // Load initial results if query exists
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');
        if (query) {
            this.searchInput.value = query;
            this.performSearch();
        }

        // Close suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.suggestionsContainer.contains(e.target)) {
                this.suggestionsContainer.classList.remove('active');
            }
        });
    }

    handleSearchInput(query) {
        clearTimeout(this.searchTimeout);
        this.currentQuery = query;

        if (query.length < 2) {
            this.suggestionsContainer.classList.remove('active');
            return;
        }

        this.searchTimeout = setTimeout(() => {
            this.loadSuggestions(query);
        }, 300);
    }

    async loadSuggestions(query) {
        try {
            const response = await fetch(`/api/videos/search/?q=${encodeURIComponent(query)}&limit=5`);
            const videos = await response.json();
            
            if (videos.length > 0) {
                this.suggestionsContainer.innerHTML = videos.map(video => `
                    <a href="/videos/${video.id}/" class="block p-3 hover:bg-white/5 border-b border-white/5 last:border-0">
                        <div class="flex items-center space-x-3">
                            <div class="w-16 h-10 bg-gray-800 rounded flex-shrink-0"></div>
                            <div class="flex-1 min-w-0">
                                <p class="font-semibold truncate">${video.title}</p>
                                <p class="text-xs text-gray-400">${video.views_count} views</p>
                            </div>
                        </div>
                    </a>
                `).join('');
                this.suggestionsContainer.classList.add('active');
            } else {
                this.suggestionsContainer.classList.remove('active');
            }
        } catch (error) {
            console.error('Error loading suggestions:', error);
        }
    }

    async performSearch() {
        const query = this.searchInput.value.trim();
        const category = document.getElementById('categoryFilter').value;
        const duration = document.getElementById('durationFilter').value;
        const date = document.getElementById('dateFilter').value;
        const premium = document.getElementById('premiumFilter').checked;
        const free = document.getElementById('freeFilter').checked;
        const sort = document.getElementById('sortFilter').value;

        // Build query params
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (category) params.append('category', category);
        if (duration) params.append('duration', duration);
        if (date) params.append('date', date);
        if (premium) params.append('premium', 'true');
        if (free) params.append('free', 'true');
        params.append('sort', sort);

        // Update URL
        window.history.pushState({}, '', `/search/?${params.toString()}`);

        // Show loading
        this.loadingState.classList.remove('hidden');
        this.resultsGrid.innerHTML = '';
        this.noResults.classList.add('hidden');
        this.suggestionsContainer.classList.remove('active');

        try {
            const response = await fetch(`/api/videos/search/?${params.toString()}`);
            const videos = await response.json();

            this.loadingState.classList.add('hidden');

            if (videos.length === 0) {
                this.noResults.classList.remove('hidden');
                this.resultsCount.textContent = 'No results found';
            } else {
                this.displayResults(videos);
                this.resultsCount.textContent = `${videos.length} video${videos.length !== 1 ? 's' : ''} found`;
            }
        } catch (error) {
            console.error('Error performing search:', error);
            this.loadingState.classList.add('hidden');
            this.noResults.classList.remove('hidden');
        }
    }

    displayResults(videos) {
        this.resultsGrid.innerHTML = videos.map(video => `
            <a href="/videos/${video.id}/" class="video-card glass-effect rounded-2xl overflow-hidden block">
                <div class="relative aspect-video">
                    ${video.thumbnail ? 
                        `<img src="${video.thumbnail}" alt="${video.title}" class="w-full h-full object-cover" loading="lazy">` :
                        `<div class="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                            <i class="fas fa-video text-5xl text-gray-600"></i>
                        </div>`
                    }
                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 p-4 flex flex-col justify-end">
                        <h3 class="font-bold mb-1 line-clamp-2">${video.title}</h3>
                        <div class="flex items-center justify-between text-xs text-gray-400">
                            <span>${video.views_count} views</span>
                            <span>${new Date(video.uploaded_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                </div>
            </a>
        `).join('');
    }

    clearFilters() {
        document.getElementById('categoryFilter').value = '';
        document.getElementById('durationFilter').value = '';
        document.getElementById('dateFilter').value = '';
        document.getElementById('premiumFilter').checked = false;
        document.getElementById('freeFilter').checked = false;
        document.getElementById('sortFilter').value = 'relevance';
        this.performSearch();
    }
}

// Initialize search when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new AdvancedSearch();
    });
} else {
    new AdvancedSearch();
}

