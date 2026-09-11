# Configuração visual e integração

Estado: editor local incluído; identidade e padrões do cliente ainda não configurados.

- Editor ou ferramenta: Editor de Carrosséis Universal.
- Localização ou URL real: `editor-carrosseis`; interface em `http://localhost:8797` quando iniciada.
- Método disponível: `editor-carrosseis/scripts/importar_carrossel.py` e operação pela interface.
- Identidade e perfil da marca:
- Templates disponíveis e linhas permitidas: Tweet (`tweet`), Stories (`stories`), Stories com Fundo (`stories-fundo`) e Bloco de Notas (`notes`). Padrão inicial: Tweet para todas as linhas; alterar quando o cliente aprovar.
- Dimensões: 4:5, com variações internas configuráveis conforme o template.
- Mapa de layouts e caixas de texto:
- Limites de texto observados:
- Áreas obrigatórias de imagem por layout:
- Fontes de imagem preferidas:
- Necessidades de crédito:
- Recorte e resolução:
- Campos e formato aceitos pelo importador: Markdown com `SLIDE N`; JSON opcional de imagens; nome e arroba por argumento.
- Comando ou procedimento verificado: `python editor-carrosseis/scripts/importar_carrossel.py <copy.md> --template <id> --profile-name "<nome>" --handle "<arroba>" [--images <imagens.json>]`.
- Onde salvar saídas: HTMLs de sessão em pasta temporária local; PNGs são exportados pelo navegador.
- Como abrir a versão recém-gerada: usar a URL retornada em JSON; não recarregar uma sessão antiga.
- Como verificar texto e imagem após importar:

O editor não inclui templates proprietários de marcas específicas. Não presuma perfil de outro cliente. Antes da primeira produção visual, preencha a identidade. Na ausência de outra escolha aprovada, use Tweet.
