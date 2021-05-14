import pandas as pd

def clean_anpocs43_data():
    df = pd.read_csv('../anpocs-scraper/output/resumos_anpocs43.csv')
    df['autores'].replace(r' ST\d\d| SPG\d\d', value='', inplace=True, regex=True)
    df['autores'] = df['autores'].str.strip()
    df['titulo'] = df['titulo'].str.strip()
    df['resumo'] = df['resumo'].str.strip()
    df['sessao'] = df['sessao'].str.strip()
    return df

def clean_anpocs44_data():
    pass

def main():
    clean_anpocs43_data()
    clean_anpocs44_data()

if __name__ == "__main__":
    main()
