# Sistema Editorial Universal

Projeto-modelo para configurar e operar um social media editorial dentro do Codex. Cada cliente recebe uma cópia independente, responde à entrevista de marca e passa a produzir conteúdos com sua própria voz, posicionamento e identidade.

## Começo rápido

1. Crie uma cópia deste repositório para o cliente.
2. Abra a pasta `projeto-cliente` como projeto local no Codex.
3. Inicie uma conversa e envie:

   > Use $social-media-editorial para configurar meu sistema editorial. Faça uma entrevista comigo, uma pergunta por vez.

4. Aprove as decisões registradas nos arquivos de cliente.
5. Depois envie `Monte a operação editorial da semana.`
6. No uso diário, envie `Execute o conteúdo de hoje.`

O guia completo está em [LEIA-ME.md](LEIA-ME.md).

## O que está incluído

- skill editorial universal em `.agents/skills/social-media-editorial`;
- documentos preenchíveis de marca, voz, formatos e identidade visual;
- curadoria, pesquisa, escrita, revisão e calendário editorial;
- editor local de carrosséis e importador de copy;
- templates Tweet, Stories, Stories com Fundo e Bloco de Notas;
- exemplos e testes automatizados.

O template ANB Style e os dados privados da operação original não fazem parte desta distribuição.

## Editor de carrosséis

No Windows, execute `projeto-cliente/editor-carrosseis/ABRIR-EDITOR.cmd`. O editor requer Python 3 e abre localmente em `http://localhost:8797`.

Para importar uma peça aprovada pelo Codex:

```powershell
python projeto-cliente/editor-carrosseis/scripts/importar_carrossel.py caminho/da-copy.md --template tweet --profile-name "Nome da Marca" --handle "arroba"
```

## Uso responsável da matriz

Mantenha este repositório como matriz. Crie uma cópia separada para cada cliente e nunca preencha a matriz com informações confidenciais. Publicação, agendamento e coleta automática de métricas não estão incluídos.
