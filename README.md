# Sistema Editorial Universal

Projeto-modelo para configurar e operar um social media editorial dentro do Codex. A skill já traz um método forte de curadoria, escrita, revisão e carrosséis; cada cliente personaliza marca, público, posicionamento, voz, oferta, CTA e identidade.

## Instalação sem conta no GitHub

1. [Baixe o pacote em ZIP](https://github.com/omatheusdeluccabusiness/sistema-editorial-universal/archive/refs/heads/main.zip).
2. Extraia o arquivo.
3. Abra **a própria pasta extraída** como projeto local no Codex. Não abra somente `editor-carrosseis`.
4. Inicie uma conversa nova e envie:

   > Use $social-media-editorial para configurar meu sistema editorial. Faça uma entrevista comigo, uma pergunta por vez.

A pasta oculta `.agents` fica na raiz e contém a skill. Não é necessário instalar globalmente nem ter conta no GitHub.

## O que mudou na versão 1.2

- a pasta baixada agora é diretamente o projeto do cliente;
- a skill está em `.agents/skills/social-media-editorial`, na raiz reconhecida pelo Codex;
- estrutura, densidade e revisão deixam de depender de campos vazios;
- storytelling e análise usam dez slides como referência;
- há faixas de palavras, regra de prosa e auditoria contra cadência picotada;
- a entrevista personaliza o método sem apagá-lo.

## Uso rápido

Depois da entrevista e de uma peça-piloto:

- `Monte a operação editorial da semana.`
- `Execute o conteúdo de hoje.`
- `Aprovado. Monte esta peça no editor usando o template configurado.`

Para conferir a instalação, use o roteiro em [TESTE-RAPIDO.md](TESTE-RAPIDO.md). O guia completo está em [LEIA-ME.md](LEIA-ME.md).

## Conteúdo do pacote

- skill editorial universal em `.agents/skills/social-media-editorial`;
- documentos preenchíveis de marca, formatos, exemplos e identidade visual;
- playbooks de storytelling, análise/opinião e notícia;
- duas revisões obrigatórias de escrita humanizada;
- calendário editorial;
- editor local de carrosséis;
- templates Tweet, Stories, Stories com Fundo e Bloco de Notas.

Templates proprietários da operação original não fazem parte desta distribuição.

## Editor de carrosséis

No Windows, execute `editor-carrosseis/ABRIR-EDITOR.cmd`. O editor requer Python 3 e abre em `http://localhost:8797`.

Importação manual:

```powershell
python editor-carrosseis/scripts/importar_carrossel.py caminho/da-copy.md --template tweet --profile-name "Nome da Marca" --handle "arroba"
```

Mantenha uma cópia separada para cada cliente. Publicação, agendamento e coleta automática de métricas não estão incluídos.
