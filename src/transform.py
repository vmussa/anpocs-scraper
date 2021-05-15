import pandas as pd

def clean_anpocs43_data():
    pass

def clean_anpocs44_data():
    df2 = pd.read_csv('../output/resumos_anpocs44.csv')
    df2['autores'] = df2['autores'].str.strip()
    df2['titulo'] = df2['titulo'].str.strip()
    df2['resumo'] = (df2['resumo']
                 .replace('^Resumo:', '', regex=True)
                 .replace('Ocultar$', '', regex=True)
                 .str.strip())
    df2['sessao'] = (df2['sessao']
                 .replace(r'(?<=GT\d\d).+|(?<=SPG\d\d).+', '', regex=True)
                 .str.strip())

def main():
    pass

if __name__ == "__main__":
    main()