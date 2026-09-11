# Sistema Editorial Universal

Base editorial e visual personalizável para mentorias. Versão 1.1, 11 de setembro de 2026.

O pacote contém um projeto-modelo pronto para ser duplicado para cada cliente. A skill conduz a configuração da marca, faz curadoria, pesquisa, escreve, revisa e mantém a fila editorial. O trabalho acontece na conversa do Codex do cliente e nos arquivos da própria cópia.

## Baixar sem conta no GitHub

O cliente pode [baixar o ZIP diretamente](https://github.com/omatheusdeluccabusiness/sistema-editorial-universal/archive/refs/heads/main.zip), extrair o arquivo e abrir `projeto-cliente` no Codex. Não precisa criar conta no GitHub. A extração deve preservar a pasta oculta `.agents`.

## Começar com um cliente

1. Duplique a pasta `projeto-cliente` e dê à cópia o nome do cliente. Preserve esta matriz para as próximas mentorias.
2. Abra essa cópia como projeto local no Codex do cliente.
3. Inicie uma conversa e peça: **Use $social-media-editorial para configurar meu sistema editorial. Faça uma entrevista comigo, uma pergunta por vez.**
4. O cliente pode responder sozinho ou junto com o mentor. Também pode fornecer materiais que já tenha.
5. Revise o documento da marca e aprove as decisões. Depois peça uma peça-piloto por vez para calibrar a escrita.
6. Quando os formatos escolhidos estiverem aprovados, peça: **Monte a operação editorial da semana.**
7. Para carrosséis aprovados, peça: **Monte esta peça no editor usando o template configurado.**

A skill está em [SKILL.md](projeto-cliente/.agents/skills/social-media-editorial/SKILL.md). A pasta oculta `.agents` faz parte do pacote e deve acompanhar a cópia. Se a skill não aparecer no Codex, abra uma nova conversa nesse projeto e confira se a extração preservou essa pasta. A instalação local segue a [documentação oficial de skills](https://learn.chatgpt.com/docs/build-skills).

## O que personalizar

O [documento da marca](projeto-cliente/.agents/skills/social-media-editorial/cliente/marca.md) reúne posicionamento, público, tensões, pilares, voz, objetivos, ofertas e CTAs. Os [formatos](projeto-cliente/.agents/skills/social-media-editorial/cliente/formatos.md) definem linhas ativas, canais, densidade, ganchos, entregas e cadência.

As referências de escrita oferecem duas revisões complementares de autoria e fluidez. Foram adaptadas para esta base: preferências de um cliente não são obrigações para todos. A orientação política, o nicho, a quantidade de slides e o estilo visual são decisões individuais.

O roteiro completo de aplicação está no [guia da mentoria](GUIA-DA-MENTORIA.md). Os critérios para testar a personalização estão nos [cenários de validação](VALIDACAO.md).

## Uso diário

- **Execute o conteúdo de hoje.**
- **Crie uma análise para o meu público e escolha a pauta.**
- **Revise este texto com minha voz.**
- **Aprovado. Registre esta versão.**
- **Essa preferência vale para todos os próximos conteúdos. Atualize a regra.**
- **Publicado. Atualize o calendário.**

A aprovação e a escolha de gancho seguem o acordo de cada cliente. O sistema não repete perguntas já respondidas nem exige um tema quando a curadoria foi delegada.

## Editor de carrosséis incluído

Cada cópia do cliente contém `editor-carrosseis`, com quatro templates:

- Modelo Tweet;
- Stories;
- Stories com Fundo;
- Bloco de Notas.

O ANB Style não está incluído. A skill pode importar a copy aprovada, inserir imagens fornecidas ou selecionadas, abrir exatamente a versão gerada e deixar a peça pronta para ajuste e exportação em PNG. No Windows, `editor-carrosseis/ABRIR-EDITOR.cmd` abre o painel local em `http://localhost:8797`.

Configure nome, arroba, template por linha e regras de imagem em [visual.md](projeto-cliente/.agents/skills/social-media-editorial/cliente/visual.md). A identidade do cliente é aplicada na importação; nenhum perfil da matriz é reutilizado.

## Entrega e limites

Inclui arquitetura editorial, entrevista, modelos preenchíveis, playbooks, revisão de escrita, operação em Markdown, editor visual, importador e quatro templates. A criação editorial em conversa não requer Python; o editor local requer Python 3 e usa somente a biblioteca padrão.

Publicação em redes, agendamento, dashboard e coleta automática de métricas não fazem parte deste pacote. A exportação dos slides é local. Integrações de Telegram, Instagram e geração de imagens exibidas em alguns templates permanecem desativadas nesta versão neutra.

A estrutura foi verificada tecnicamente. A voz de cada cliente precisa ser validada com conteúdo real; essa aprovação não pode ser herdada de outro projeto.

## Preparar para GitHub depois

O pacote contém apenas a base neutra. Trabalhe com cópias de clientes fora da matriz. Antes de publicar uma cópia preenchida, retire os materiais privados e obtenha autorização para compartilhar exemplos. Não foi criado repositório nem enviada informação a serviço externo nesta entrega.
