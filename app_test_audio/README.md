# Test Auditif - Audio Steganography

Application de tests auditifs pour évaluer la ressemblance entre un son de référence et plusieurs variantes encodées.

---

## 📋 Prérequis (si exécution avec Python)

- **Python 3.8+** installé
- **Bibliothèques Python** :
  - `pygame`
  - `tkinter` (inclus par défaut avec Python sur la plupart des plateformes)

Un fichier `requirements.txt` est fourni :

```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

1. **Télécharger le dépot**
```bash
mkdir <nom-du-repo>
cd <nom-du-repo>
```

2. **Créer et activer un environnement virtuel**
```bash
python -m venv venv        # création
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

---

## ▶️ Lancement

### Avec Python

```bash
python audio_test_app.py
```

### En stand‑alone (Windows avec PyInstaller)

Si vous disposez de l’exécutable généré (`dist/audio_test_app.exe`), double‑cliquez simplement sur `audio_test_app.exe`, ou lancez‑le depuis un terminal :

```powershell
cd dist
./audio_test_app.exe
```


---

## 🖥️ Utilisation

1. **Saisir l’ID du sujet** dans le champ prévu.
2. **Cliquer sur "Charger dossier de tests"** et sélectionner le dossier **tests** contenant vos sous‑dossiers de sons.
3. **Naviguer dans les onglets** (un onglet par condition/dossier).
4. Pour chaque fichier :
   - ▶️ **Lecture** du son (bouton ▶)
   - ■ **Arrêt** de la lecture (bouton ■)
   - **Noter la ressemblance** via le slider (0 = différent, 100 = identique)
5. **Enregistrer les résultats** dans un CSV via le bouton "Enregistrer".

Les résultats sont exportés sous la forme :

| subject_id | folder      | file            | score |
|------------|-------------|-----------------|-------|
| ABC123     | ConditionA  | sample_A2.wav   | 85    |
| ABC123     | ConditionA  | sample_A3.wav   | 70    |
| ...        | ...         | ...             | ...   |


# Retourner le fichier .csv contenant vos réponses

Enregistrer votre fichier de réponse sous le nom **test_stegano_nom_prenom.csv**
