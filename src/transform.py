import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = f"{BASE_PATH}{os.sep}output{os.sep}"


def clean_anpocs43_data():
    df = pd.read_csv(f'{OUTPUT_PATH}resumos_anpocs43.csv')
    df['autores'].replace(r' ST\d\d| SPG\d\d', value='', inplace=True, regex=True)
    df['autores'] = df['autores'].str.strip()
    df['titulo'] = df['titulo'].str.strip()
    df['resumo'] = df['resumo'].str.strip()
    df['sessao'] = df['sessao'].str.strip()
    return df


def clean_anpocs44_data():
    df = pd.read_csv(f'{OUTPUT_PATH}resumos_anpocs44.csv')
    df['autores'] = df['autores'].str.strip()
    df['titulo'] = df['titulo'].str.strip()
    df['resumo'] = (df['resumo']
                    .replace('^Resumo:', '', regex=True)
                    .replace('Ocultar$', '', regex=True)
                    .str.strip()
                    .apply(lambda x: " ".join(x.split('\n'))))
    df['sessao'] = (df['sessao']
                    .replace(r'(?<=GT\d\d).+|(?<=SPG\d\d).+', '', regex=True)
                    .str.strip())
    return df


def main():
    anpocs43 = clean_anpocs43_data()
    anpocs44 = clean_anpocs44_data()
    df = pd.concat([anpocs43, anpocs44]).reset_index(drop=True)
    df.to_csv(f'{OUTPUT_PATH}resumos_anpocs.csv')


if __name__ == "__main__":
    main()
