# Raspador dos Encontros Anuais da ANPOCS
O `anpocs-scraper` é um raspador dos dados dos [Encontros Anuais da ANPOCS](http://anpocs.com/index.php/encontros/apresentacao) escrito em Python. Atualmente o código permite coletar:
* os dados de todos os resumos dos trabalhos apresentados em GT's e SPG's do [44º Encontro Anual da ANPOCS](https://www.anpocs2020.sinteseeventos.com.br/)
* os dados de todos os resumos dos trabalhos apresentados em ST's e SPG's do [43º Encontro Anual da ANPOCS](http://anpocs.com/index.php/43-encontro-anual-2019/2750-encontros-anuais/43-encontro/2301-resumos-sts-e-spgs)

# Instalação e modo de uso
Para instalar o raspador basta clonar o presente repositório e instalar suas dependências:
```
git clone https://github.com/vmussa/anpocs-scraper
cd anpocs-scraper
python -m venv .venv
pip install -r requirements.txt
```
Para rodar o raspador, continue no repositório clonado e execute o código `main.py` com o Python:
```
python src/main.py
```

# Em breve
Futuramente o raspador abarcará todos os GT's e SPG's do encontro 45, cujos resumos dos trabalhos estarão disponíveis [aqui](https://www.anpocs2021.sinteseeventos.com.br/).

# Autores
[Vítor Mussa](https://vmussa.github.io/) (@vmussa) e Daniel Mendes (@danielmnds34).

# Agradecimentos
Agradecemos à ANPOCS, à CAPES, ao PPGSA/UFRJ e aos laboratórios de pesquisa [LABHD/UFBA](http://www.labhd.ufba.br/) e DTA/UFRJ.