# Streamlit for cotomi demo

## Operation

- Don't hardcode, use environment-values
- When you add or change environment-values:
    - Change config.py
    - Change .env.local

## Files

- `streamlit/`: projects build directory
    - `streamlit/`
        - `notebooks/` testing notebook files as memo
        - `pages/`
            - `Archive/` Unneeded used files
            - `src/`
                - `utils/` utility files such as components.py
                - `each_model.py` each model generation files
            - `each_model.py` each model page name files
        - `tests/` test files
        - `config.py`
        - `cotomi_core_light.py` this is main file
    - `Dockerfile`
    - `requirements.txt`
- `.env`
- `.env.local` template file of .env
- `.compose.yaml`
