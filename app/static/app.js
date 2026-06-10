(() => {
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const uploadContent = document.getElementById('uploadContent');
  const uploadPreview = document.getElementById('uploadPreview');
  const previewImage = document.getElementById('previewImage');
  const removeBtn = document.getElementById('removeBtn');
  const uploadStatus = document.getElementById('uploadStatus');
  const spinner = document.getElementById('spinner');
  const statusText = document.getElementById('statusText');
  const errorBanner = document.getElementById('errorBanner');
  const errorMessage = document.getElementById('errorMessage');
  const retryBtn = document.getElementById('retryBtn');
  const resultsSection = document.getElementById('resultsSection');
  const resultsGrid = document.getElementById('resultsGrid');
  const resultsMeta = document.getElementById('resultsMeta');

  let currentFile = null;
  let isUploading = false;

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.hidden = false;
    uploadStatus.hidden = true;
  }

  function hideError() {
    errorBanner.hidden = true;
  }

  function setLoading(loading) {
    isUploading = loading;
    spinner.hidden = !loading;
    statusText.textContent = loading ? 'Identifying…' : '';
    uploadStatus.hidden = !loading;
  }

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      uploadContent.hidden = true;
      uploadPreview.hidden = false;
      dropZone.classList.remove('dragover');
    };
    reader.readAsDataURL(file);
  }

  function removePreview() {
    currentFile = null;
    previewImage.src = '';
    uploadPreview.hidden = true;
    uploadContent.hidden = false;
    hideError();
    resultsSection.hidden = true;
  }

  function renderSkeletons() {
    resultsGrid.innerHTML = `
      <div class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-line w-60"></div>
        <div class="skeleton-line w-40"></div>
        <div class="skeleton-line w-50"></div>
      </div>
      <div class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-line w-60"></div>
        <div class="skeleton-line w-40"></div>
        <div class="skeleton-line w-50"></div>
      </div>
      <div class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-line w-60"></div>
        <div class="skeleton-line w-40"></div>
        <div class="skeleton-line w-50"></div>
      </div>`;
    resultsSection.hidden = false;
  }

  function confidenceClass(score) {
    if (score >= 0.9) return 'high';
    if (score >= 0.7) return 'medium';
    return 'low';
  }

  function confidencePct(score) {
    return Math.round(score * 100);
  }

  function formatPrice(v) {
    if (v == null) return '—';
    return `$${v.toFixed(2)}`;
  }

  function renderResults(matches, elapsed) {
    resultsMeta.textContent = `${matches.length} match${matches.length !== 1 ? 'es' : ''} · ${elapsed}s`;

    resultsGrid.innerHTML = matches.map((m, i) => {
      const confClass = confidenceClass(m.confidence);
      const confPct = confidencePct(m.confidence);
      const imgSrc = m.thumbnail_url || m.image_url || '';
      const cat = m.category || m.item_type;

      const newMin = formatPrice(m.pricing?.new_min_price);
      const newSellers = m.pricing?.new_sellers != null ? m.pricing.new_sellers : '—';
      const usedMin = formatPrice(m.pricing?.used_min_price);
      const usedSellers = m.pricing?.used_sellers != null ? m.pricing.used_sellers : '—';
      const hasPricing = m.pricing && (m.pricing.new_min_price != null || m.pricing.used_min_price != null);

      const setsHtml = m.set_appearances?.length
        ? `<details class="set-appearances">
            <summary>In ${m.set_appearances.length} set${m.set_appearances.length !== 1 ? 's' : ''}</summary>
            <ul class="set-list">${m.set_appearances.map(s => `<li>${s.name}</li>`).join('')}</ul>
          </details>`
        : '';

      const pricingHtml = hasPricing
        ? `<div class="card-pricing">
            <div class="price-row"><span class="price-label">New from</span><span class="price-value">${newMin}</span></div>
            <div class="price-row"><span class="price-label">Sellers</span><span class="price-value">${newSellers}</span></div>
            <div class="price-row"><span class="price-label">Used from</span><span class="price-value">${usedMin}</span></div>
            <div class="price-row"><span class="price-label">Sellers</span><span class="price-value">${usedSellers}</span></div>
          </div>`
        : '';

      return `<div class="result-card">
        <div class="card-img-wrap">
          ${imgSrc ? `<img src="${imgSrc}" alt="${m.name}" loading="lazy">` : '<div style="padding:40px;text-align:center;color:var(--text-dim)">No image</div>'}
          <span class="confidence-badge ${confClass}">${confPct}%</span>
        </div>
        <div class="card-body">
          <div class="card-title">${m.name}</div>
          <div class="card-number">#${m.item_no}</div>
          <span class="card-category">${cat}</span>
          ${pricingHtml}
          ${setsHtml}
          <div class="card-actions">
            <a href="${m.bricklink_url}" target="_blank" class="btn-bl">BrickLink</a>
            <a href="${m.rebrickable_url}" target="_blank" class="btn-rb">Rebrickable</a>
          </div>
        </div>
      </div>`;
    }).join('');
  }

  async function upload(file) {
    if (isUploading) return;
    hideError();
    renderSkeletons();

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const resp = await fetch('/upload', { method: 'POST', body: formData });
      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(text || `Server error ${resp.status}`);
      }
      const data = await resp.json();
      if (!data.matches?.length) {
        showError('No matches found. Try a different photo or lighting.');
        resultsSection.hidden = true;
        return;
      }
      renderResults(data.matches, data.processing_time);
    } catch (err) {
      showError(err.message || 'Upload failed. Is the server running?');
      resultsSection.hidden = true;
    } finally {
      setLoading(false);
    }
  }

  function handleFile(file) {
    if (!file) return;
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      showError('Please select a JPEG or PNG image.');
      return;
    }
    if (file.size > 20 * 1024 * 1024) {
      showError('Image must be under 20 MB.');
      return;
    }
    currentFile = file;
    hideError();
    showPreview(file);
    upload(file);
  }

  // Drag and drop
  dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
  dropZone.addEventListener('drop', (e) => { e.preventDefault(); dropZone.classList.remove('dragover'); handleFile(e.dataTransfer.files[0]); });

  // Click to browse
  dropZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => handleFile(fileInput.files[0]));

  // Remove
  removeBtn.addEventListener('click', (e) => { e.stopPropagation(); removePreview(); });

  // Retry
  retryBtn.addEventListener('click', () => { if (currentFile) upload(currentFile); });
})();
