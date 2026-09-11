# Sistema Editorial Universal

Base editorial e visual personalizável para mentorias. Versão 1.2, 11 de setembro de 2026.

O pacote é simultaneamente um projeto de cliente e uma skill local do Codex. Ele não entrega uma folha em branco: já contém a arquitetura de produção que controla prosa, densidade, retenção, clareza e revisão. A entrevista serve para ensinar a identidade de cada marca.

## Baixar e abrir

O cliente pode [baixar o ZIP diretamente](https://github.com/omatheusdeluccabusiness/sistema-editorial-universal/archive/refs/heads/main.zip), extrair e abrir **a pasta extraída inteira** no Codex. Não precisa criar conta no GitHub.

Na raiz precisam aparecer `.agents`, `editor-carrosseis`, `operacao` e este arquivo. Se a pasta `.agents` não estiver presente, a extração ficou incompleta.

## Primeira conversa

Envie:

> Use $social-media-editorial para configurar meu sistema editorial. Faça uma entrevista comigo, uma pergunta por vez.

O cliente pode responder sozinho ou com o mentor. Se já houver briefing, posts aprovados e materiais de voz, anexe-os. A skill registra as decisões em [marca.md](.agents/skills/social-media-editorial/cliente/marca.md) e [formatos.md](.agents/skills/social-media-editorial/cliente/formatos.md).

Os formatos já têm padrões ativos. O cliente só precisa aprovar ou alterar o que for particular. Não deixe “quantidade de texto” em aberto esperando que o modelo adivinhe.

## Calibração

1. Termine o mínimo da entrevista: público, objetivo, pilares, voz, posicionamento e CTA.
2. Peça uma peça inédita por vez.
3. Dê feedback concreto sobre gancho, fluidez, densidade e vocabulário.
4. Quando uma correção valer para o futuro, diga: `Esta preferência é permanente. Atualize a regra e registre o exemplo.`
5. Teste outro tema para verificar se o padrão se repete.

Os padrões de fábrica usam carrosséis de storytelling, análise/opinião e notícia. A marca pode desativar qualquer linha ou ativar outros meios.

## Uso diário

- `Monte a operação editorial da semana.`
- `Execute o conteúdo de hoje.`
- `Crie uma análise para o meu público e escolha a pauta.`
- `Revise este texto com a voz da marca.`
- `Aprovado. Registre esta versão.`
- `Aprovado. Monte no editor.`
- `Publicado. Atualize o calendário.`

## Editor incluído

O pacote contém os templates Tweet, Stories, Stories com Fundo e Bloco de Notas. No Windows, `editor-carrosseis/ABRIR-EDITOR.cmd` abre o painel em `http://localhost:8797`.

Configure nome, arroba e preferências em [visual.md](.agents/skills/social-media-editorial/cliente/visual.md). O template padrão é Tweet até que o cliente aprove outro.

O editor pode importar a copy aprovada e imagens, abrir a versão recém-gerada e exportar PNG. Templates proprietários de marcas específicas não estão incluídos.

## Diagnóstico

Se a resposta parecer genérica, envie:

> Use $social-media-editorial e informe quais arquivos de configuração você carregou, quais padrões editoriais estão ativos e o que ainda não foi configurado. Não produza conteúdo ainda.

O resultado esperado está em [TESTE-RAPIDO.md](TESTE-RAPIDO.md). A skill está em [SKILL.md](.agents/skills/social-media-editorial/SKILL.md).

## Limites

Publicação em redes, agendamento, dashboard e coleta automática de métricas não fazem parte do pacote. A criação editorial não exige Python; o editor local exige Python 3.

A skill pode reproduzir o método, mas a voz precisa ser calibrada com exemplos reais de cada cliente. Nunca coloque dados privados de um cliente na matriz pública.
