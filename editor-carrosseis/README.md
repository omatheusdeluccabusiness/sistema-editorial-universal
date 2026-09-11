# Editor de Carrosséis Universal

Editor local incluído no Sistema Editorial Universal. Ele contém quatro templates: Tweet, Stories, Stories com Fundo e Bloco de Notas. O ANB Style não faz parte desta distribuição.

## Abrir no Windows

Clique duas vezes em `ABRIR-EDITOR.cmd`. O painel abre em `http://localhost:8797`. Para encerrar o serviço, use `PARAR-EDITOR.cmd`.

É necessário ter Python 3 instalado. O editor usa somente a biblioteca padrão do Python e não exige instalação de pacotes.

## Importar uma peça aprovada

O Markdown precisa conter blocos consecutivos:

```md
# Título da peça

## SLIDE 1
Texto da capa.

## SLIDE 2
Texto do segundo slide.

## SLIDE 3
Texto do terceiro slide.

## LEGENDA
Legenda da publicação.
```

Execute:

```powershell
py -3 scripts/importar_carrossel.py exemplos/carrossel-exemplo.md --template tweet --profile-name "Nome da Marca" --handle "nomedamarca"
```

Para inserir imagens, crie um JSON com URL ou caminho local:

```json
{
  "1": "https://exemplo.com/capa.jpg",
  "3": "C:/Imagens/slide-3.png"
}
```

Acrescente `--images caminho/do/imagens.json`. O importador devolve uma resposta JSON com a URL exata da nova sessão.

## Escopo

O fluxo incluído cobre montagem, edição visual e exportação dos PNGs. Publicação em redes sociais, Telegram e geração interna de imagens são integrações opcionais e estão desativadas no pacote neutro.
