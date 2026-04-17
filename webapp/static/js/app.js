/**
 * FloodWatch - Dashboard JavaScript
 * Minimalist & Classy Web Application
 * Optimized for Performance
 */

// ============================================
// Configuration
// ============================================

const API_BASE = '';
const CACHE_TIMEOUT = 60000; // 1 minute cache
const cache = new Map();

const DISTRICTS = {
    'Chennai': { lat: 13.0827, lon: 80.2707, color: '#3B82F6' },
    'Tiruvallur': { lat: 13.1432, lon: 79.9089, color: '#10B981' },
    'Chengalpattu': { lat: 12.6921, lon: 79.9779, color: '#F59E0B' },
    'Kancheepuram': { lat: 12.8342, lon: 79.7036, color: '#EF4444' },
    'Cuddalore': { lat: 11.7480, lon: 79.7714, color: '#8B5CF6' },
    'Nagapattinam': { lat: 10.7672, lon: 79.8449, color: '#EC4899' }
};

// ============================================
// DOM Elements
// ============================================

const elements = {
    districtGrid: document.getElementById('district-grid'),
    districtSelect: document.getElementById('district-select'),
    analysisContent: document.getElementById('analysis-content'),
    refreshBtn: document.getElementById('refresh-btn'),
    loadingOverlay: document.getElementById('loading-overlay'),
    totalRecords: document.getElementById('total-records')
};

// ============================================
// Utility Functions
// ============================================

function showLoading() {
    elements.loadingOverlay.classList.add('active');
}

function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatPercent(value) {
    return (value * 100).toFixed(1) + '%';
}

function getRiskClass(level) {
    return level.toLowerCase();
}

function getCached(key) {
    const cached = cache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TIMEOUT) {
        return cached.data;
    }
    cache.delete(key);
    return null;
}

function setCache(key, data) {
    cache.set(key, { data, timestamp: Date.now() });
}

// ============================================
// API Functions with Error Handling & Caching
// ============================================

async function fetchWithCache(url, cacheKey) {
    // Check cache first
    const cached = getCached(cacheKey);
    if (cached) return cached;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        setCache(cacheKey, data);
        return data;
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        return null;
    }
}

async function fetchAllPredictions() {
    return fetchWithCache(`${API_BASE}/api/predict/all`, 'predictions-all');
}

async function fetchDistrictPrediction(district) {
    return fetchWithCache(
        `${API_BASE}/api/predict/${encodeURIComponent(district)}`,
        `prediction-${district}`
    );
}

async function fetchHistory(district) {
    return fetchWithCache(
        `${API_BASE}/api/history/${encodeURIComponent(district)}`,
        `history-${district}`
    );
}

async function fetchStats() {
    return fetchWithCache(`${API_BASE}/api/stats`, 'stats');
}

// ============================================
// UI Rendering Functions
// ============================================

function createDistrictCard(district, data) {
    const riskLevel = data.risk_level || 'LOW';
    const riskClass = getRiskClass(riskLevel);
    const ensembleProb = data.ensemble || 0;
    const weather = data.weather || {};
    const coords = DISTRICTS[district];

    return `
        <div class="district-card" data-district="${district}" style="--card-accent: ${coords.color}">
            <div class="district-header">
                <div>
                    <h3 class="district-name">${district}</h3>
                    <p class="district-coords">${coords.lat.toFixed(4)}°N, ${coords.lon.toFixed(4)}°E</p>
                </div>
                <span class="risk-badge ${riskClass}">${riskLevel}</span>
            </div>
            
            <div class="risk-meter">
                <div class="risk-meter-label">
                    <span class="risk-meter-text">Flood Risk Probability</span>
                    <span class="risk-meter-value">${formatPercent(ensembleProb)}</span>
                </div>
                <div class="risk-meter-bar">
                    <div class="risk-meter-fill ${riskClass}" style="width: ${ensembleProb * 100}%"></div>
                </div>
            </div>
            
            <div class="weather-info">
                <div class="weather-item">
                    <div class="weather-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
                        </svg>
                    </div>
                    <div class="weather-data">
                        <span class="weather-value">${weather.rainfall?.toFixed(1) || '0.0'} mm</span>
                        <span class="weather-label">Rainfall</span>
                    </div>
                </div>
                <div class="weather-item">
                    <div class="weather-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>
                        </svg>
                    </div>
                    <div class="weather-data">
                        <span class="weather-value">${weather.temperature?.toFixed(1) || '0.0'}°C</span>
                        <span class="weather-label">Temperature</span>
                    </div>
                </div>
                <div class="weather-item">
                    <div class="weather-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                        </svg>
                    </div>
                    <div class="weather-data">
                        <span class="weather-value">${(weather.soil_moisture * 100)?.toFixed(0) || '0'}%</span>
                        <span class="weather-label">Soil Moisture</span>
                    </div>
                </div>
                <div class="weather-item">
                    <div class="weather-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
                        </svg>
                    </div>
                    <div class="weather-data">
                        <span class="weather-value">${weather.humidity?.toFixed(0) || '0'}%</span>
                        <span class="weather-label">Humidity</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function renderDistrictCards(predictions) {
    if (!predictions) {
        elements.districtGrid.innerHTML = '<p class="placeholder-message">Error loading data</p>';
        return;
    }

    let html = '';
    for (const district of Object.keys(DISTRICTS)) {
        const data = predictions[district] || {};
        html += createDistrictCard(district, data);
    }

    elements.districtGrid.innerHTML = html;

    // Add click listeners
    document.querySelectorAll('.district-card').forEach(card => {
        card.addEventListener('click', () => {
            const district = card.dataset.district;
            elements.districtSelect.value = district;
            loadDistrictAnalysis(district);

            // Scroll to analysis
            document.getElementById('analysis').scrollIntoView({ behavior: 'smooth' });
        });
    });
}

function renderAnalysisPanel(district, prediction, history) {
    const models = ['transformer', 'lstm', 'xgboost', 'random_forest'];

    let modelPredictionsHTML = '';
    models.forEach(model => {
        const value = prediction[model];
        if (value !== undefined) {
            const modelName = model.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            modelPredictionsHTML += `
                <div class="prediction-row">
                    <span class="prediction-model">${modelName}</span>
                    <span class="prediction-value">${formatPercent(value)}</span>
                </div>
            `;
        }
    });

    // Add ensemble
    if (prediction.ensemble) {
        modelPredictionsHTML += `
            <div class="prediction-row" style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2);">
                <span class="prediction-model" style="font-weight: 600;">Ensemble Average</span>
                <span class="prediction-value" style="color: #3B82F6;">${formatPercent(prediction.ensemble)}</span>
            </div>
        `;
    }

    // History chart
    let historyChartHTML = '';
    if (history && history.rainfall) {
        const maxRainfall = Math.max(...history.rainfall, 1);
        history.rainfall.forEach((rainfall, i) => {
            const height = (rainfall / maxRainfall) * 100;
            const isFlood = history.flood_risk[i] === 1;
            historyChartHTML += `<div class="chart-bar ${isFlood ? 'flood' : ''}" style="height: ${Math.max(height, 2)}%" title="${history.dates[i]}: ${rainfall.toFixed(1)}mm"></div>`;
        });
    }

    elements.analysisContent.innerHTML = `
        <div class="analysis-grid">
            <div class="analysis-card">
                <h4 class="analysis-card-title">Model Predictions</h4>
                <div class="model-predictions">
                    ${modelPredictionsHTML}
                </div>
            </div>
            
            <div class="analysis-card">
                <h4 class="analysis-card-title">Current Conditions</h4>
                <div class="model-predictions">
                    <div class="prediction-row">
                        <span class="prediction-model">Rainfall</span>
                        <span class="prediction-value">${prediction.weather?.rainfall?.toFixed(1) || '0'} mm</span>
                    </div>
                    <div class="prediction-row">
                        <span class="prediction-model">Soil Moisture</span>
                        <span class="prediction-value">${((prediction.weather?.soil_moisture || 0) * 100).toFixed(1)}%</span>
                    </div>
                    <div class="prediction-row">
                        <span class="prediction-model">Temperature</span>
                        <span class="prediction-value">${prediction.weather?.temperature?.toFixed(1) || '0'}°C</span>
                    </div>
                    <div class="prediction-row">
                        <span class="prediction-model">Humidity</span>
                        <span class="prediction-value">${prediction.weather?.humidity?.toFixed(0) || '0'}%</span>
                    </div>
                    <div class="prediction-row">
                        <span class="prediction-model">Last Updated</span>
                        <span class="prediction-value">${prediction.weather?.date || 'N/A'}</span>
                    </div>
                </div>
            </div>
            
            <div class="analysis-card" style="grid-column: span 2;">
                <h4 class="analysis-card-title">30-Day Rainfall History</h4>
                <div class="history-chart">
                    ${historyChartHTML || '<p style="color: var(--text-muted);">No history data available</p>'}
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
                    <span>${history?.dates?.[0] || ''}</span>
                    <span>Red bars indicate flood events</span>
                    <span>${history?.dates?.[history.dates.length - 1] || ''}</span>
                </div>
            </div>
        </div>
    `;
}

// ============================================
// Data Loading Functions
// ============================================

async function loadDashboard() {
    showLoading();

    try {
        // Load stats
        const stats = await fetchStats();
        if (stats) {
            elements.totalRecords.textContent = formatNumber(stats.total_records);
        }

        // Load predictions
        const predictions = await fetchAllPredictions();
        renderDistrictCards(predictions);

    } catch (error) {
        console.error('Error loading dashboard:', error);
    } finally {
        hideLoading();
    }
}

async function loadDistrictAnalysis(district) {
    showLoading();

    try {
        const [prediction, history] = await Promise.all([
            fetchDistrictPrediction(district),
            fetchHistory(district)
        ]);

        renderAnalysisPanel(district, prediction, history);

    } catch (error) {
        console.error('Error loading district analysis:', error);
    } finally {
        hideLoading();
    }
}

// ============================================
// Event Listeners
// ============================================

elements.refreshBtn.addEventListener('click', async () => {
    elements.refreshBtn.classList.add('loading');
    await loadDashboard();
    elements.refreshBtn.classList.remove('loading');
});

elements.districtSelect.addEventListener('change', (e) => {
    const district = e.target.value;
    if (district) {
        loadDistrictAnalysis(district);
    }
});

// Smooth scroll for navigation links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }

            // Update active state
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
});

// ============================================
// Initialize
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});

