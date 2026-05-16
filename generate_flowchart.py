import base64
import urllib.request

mermaid_code = """graph TD
    A["EEG Dataset Collection\nBonn Dataset - 11,500 samples x 178 features"] --> B["Data Preprocessing\nRemove index, Z-Score Normalization"]
    B --> C["Data Splitting\n80% Train, 10% Val, 10% Test"]
    C --> D1["1D Signal to 2D Spectrogram\nSTFT, Log scaling, Resize 64x64"]
    C --> D2["1D Signal Reshaping\nReshape to (178, 1)"]
    D1 --> E1["VGG16 (Frozen)\nSpatial Features"]
    D1 --> E2["ResNet50 (Frozen)\nSpatial Features"]
    D2 --> E3["1D-CNN + Bi-LSTM\nTemporal Features"]
    E1 --> F["Feature Fusion\nConcatenation"]
    E2 --> F
    E3 --> F
    F --> G["Classification\nDense(512)->Dense(256)->Softmax(5)"]
    G --> H["Evaluation\nAccuracy, Confusion Matrix, etc."]

    classDef lb fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef lg fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef ly fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef lo fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef lp fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef lr fill:#ffebee,stroke:#c62828,stroke-width:2px;
    class A lb;
    class B,H lg;
    class C ly;
    class D1,D2 lo;
    class E1,E2,E3 lp;
    class F lr;
    class G lb;
"""

# Mermaid.ink requires URL-safe base64 encoding without padding
b64 = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8').rstrip('=')
url = f"https://mermaid.ink/img/{b64}?type=jpeg&bgColor=FFFFFF"

print("Downloading from", url)
req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
)

try:
    with urllib.request.urlopen(req) as response, open("methodology_flowchart.jpeg", "wb") as out_file:
        out_file.write(response.read())
    print("Successfully saved methodology_flowchart.jpeg")
except Exception as e:
    print("Error:", e)
