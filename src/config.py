from pathlib import Path
import nltk

# 1. Rutas absolutas del proyecto
# __file__ apunta a config.py, .parent es 'src', y el segundo .parent es la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# 2. Configuración inicial de NLP
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# 3. Constantes globales
# Usaremos inglés ya que la mayoría de artículos científicos sobre IA están en este idioma
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))