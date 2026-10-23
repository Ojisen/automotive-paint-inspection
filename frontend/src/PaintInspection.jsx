const PAINT_API_BASES = ['http://127.0.0.1:8000', 'http://localhost:8000'];

function PaintInspection() {
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [previewUrl, setPreviewUrl] = React.useState(null);
  const [result, setResult] = React.useState(null);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const fileInputRef = React.useRef(null);

  React.useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const selectFile = (file) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setSelectedFile(null);
    setResult(null);
    setErrorMessage('');

    if (!file) return;

    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      setErrorMessage('Formats acceptés : JPEG et PNG uniquement.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const onFileSelected = (event) => {
    selectFile(event.target.files?.[0] || null);
    event.target.value = '';
  };

  const analyze = async () => {
    if (!selectedFile || isLoading) return;

    setIsLoading(true);
    setResult(null);
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    let response = null;
    let lastError = null;

    for (const baseUrl of PAINT_API_BASES) {
      try {
        response = await fetch(`${baseUrl}/paint/predict`, {
          method: 'POST',
          body: formData,
        });
        break;
      } catch (error) {
        lastError = error;
      }
    }

    try {
      if (!response) {
        throw new Error(lastError?.message || 'Backend inaccessible.');
      }

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.message || 'Erreur du serveur.');
      }

      setResult(data);
    } catch (error) {
      setErrorMessage(
        error.message || "Impossible de contacter le serveur d'analyse peinture."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setErrorMessage('');
    setIsLoading(false);
  };

  return (
    <main className="paint-page">
      <section className="paint-shell">
        <header className="paint-header">
          <p className="paint-eyebrow">Modèle expérimental</p>
          <h1>Classification de peinture automobile</h1>
          <p className="paint-intro">
            Soumettez une image macro pour estimer si la peinture est d'origine ou repeinte.
          </p>
        </header>

        <section className="paint-workspace">
          <div className="paint-left-column">
            <section className="paint-input-card">
              <label className="file-picker">
                <span className="picker-title">Choisir une image</span>
                <span className="picker-hint">
                JPEG ou PNG, une seule image, 10 MB maximum
                </span>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png"
                  onChange={onFileSelected}
                />
              </label>

              {previewUrl ? (
                <>
                  <div className="preview-frame">
                    <img src={previewUrl} alt="Image originale sélectionnée" />
                  </div>
                  <p className="file-name">{selectedFile?.name}</p>
                </>
              ) : (
                <div className="empty-preview">Aucun aperçu disponible</div>
              )}

              {!result && (
                <button
                  className="validate-button"
                  type="button"
                  disabled={!selectedFile || isLoading}
                  onClick={analyze}
                >
                  {isLoading ? 'Analyse en cours...' : "Valider l'image"}
                </button>
              )}

              {isLoading && (
                <p className="paint-loading-message" role="status">
                  Le modèle analyse votre image...
                </p>
              )}

              {errorMessage && (
                <p className="paint-error-message" role="alert">
                  {errorMessage}
                </p>
              )}
            </section>

            {result?.cropped_image && (
              <section className="paint-crop-card">
                <h2>Zone utilisée par le modèle</h2>
                <div className="crop-preview-frame">
                  <img
                    src={result.cropped_image}
                    alt="Zone centrale utilisée par le modèle"
                  />
                </div>
                <p className="crop-note">
                  Les bords périphériques sont retirés avant l'inférence afin de
                  limiter l'influence du vignettage et du cercle lumineux.
                </p>
              </section>
            )}
          </div>

          <aside className="result-panel" aria-live="polite">
            {result ? (
              <div className={`paint-result-card verdict-${result.verdict}`}>
                <p className="paint-eyebrow">Résultat</p>
                <h2>{result.verdict}</h2>

                <div className="paint-confidence">
                  <span>Confiance</span>
                  <strong>{Math.round(result.confidence * 100)}%</strong>
                </div>

                {[
                  ['Origine', result.probabilities.origine, 'origine'],
                  ['Repeint', result.probabilities.repeint, 'repeint'],
                ].map(([label, probability, type]) => (
                  <div className="paint-probability-row" key={type}>
                    <div>
                      <span>{label}</span>
                      <strong>{Math.round(probability * 100)}%</strong>
                    </div>
                    <div className={`paint-probability-bar ${type}`}>
                      <span style={{ width: `${probability * 100}%` }} />
                    </div>
                  </div>
                ))}

                <p className="paint-experimental-note">
                  Résultat expérimental, modèle {result.model_version}
                </p>
                <button className="paint-reset-button" type="button" onClick={reset}>
                  Nouvelle analyse
                </button>
              </div>
            ) : (
              <div className="paint-result-placeholder">
                <span>01</span>
                <h2>Votre résultat apparaîtra ici</h2>
                <p>Sélectionnez une image puis validez-la pour lancer l'inférence.</p>
              </div>
            )}
          </aside>
        </section>
      </section>
    </main>
  );
}

window.PaintInspection = PaintInspection;