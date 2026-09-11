# Distribuição visual e imagens

O pacote inclui um editor local em `editor-carrosseis`. Use a configuração de `visual.md` para selecionar o template, a identidade, as imagens e o caminho de saída. Outra ferramenta só pode substituir essa integração depois de ser inspecionada e registrada.

## Texto nas caixas

Leia o layout efetivo, não apenas o número do slide. Identifique título, corpo, complemento, legenda ou outra área existente. Distribua a copy aprovada em cortes naturais, preservando palavras, ordem, informações e ausência de duplicação.

Uma caixa adicional não exige uma frase nova. Uma caixa de destaque pode receber uma parte já escrita, desde que a leitura na ordem do layout preserve o sentido. Não invente subtítulos nem resuma texto aprovado para acomodar um campo.

Se não couber, indique o conflito e proponha ajuste de layout ou edição mínima. Não anuncie montagem pronta antes de verificar a versão renderizada.

## Imagens

Siga a função visual de cada layout e as preferências do cliente. Em layouts que exigem fotografia ou faixa de imagem, pesquise uma imagem relacionada ao conteúdo para cada área obrigatória. Em layouts opcionais, uma imagem genérica pode ser pior que uma composição tipográfica.

Pinterest pode ser uma camada de descoberta, junto a busca de imagens, acervos e fontes originais. Pesquise a cena, objeto, época e função visual do slide, com variações de consulta quando necessário. Compare candidatas por pertinência, resolução, legibilidade, recorte e consistência entre slides. Evite repetição e imagens que representem falsamente o fato.

Não presuma licença livre. Respeite créditos e condições aplicáveis. Não imponha ao cliente um relatório extra de curadoria quando não for necessário à entrega.

## Conferência

Verifique texto, quantidade de slides, identificação da marca, imagens obrigatórias, enquadramento e legibilidade. Abra exatamente a saída recém-gerada. Sem acesso à ferramenta ou sem imagem necessária, entregue a parte pronta e informe a pendência, sem afirmar que a integração foi concluída.

## Importação incluída

O arquivo-fonte precisa conter blocos `SLIDE N` consecutivos. O manifesto opcional de imagens é um objeto JSON como `{"1": "https://...", "3": "C:/.../imagem.jpg"}`. O importador aceita os templates `tweet`, `stories`, `stories-fundo` e `notes`, inicia o servidor local, gera uma URL exclusiva e pode abrir essa versão no navegador.

Comando-base:

`python editor-carrosseis/scripts/importar_carrossel.py producoes/peca.md --template tweet --profile-name "Nome da Marca" --handle "arroba" --images producoes/imagens.json`

As quatro opções são neutras e reutilizáveis. O template proprietário ANB Style não integra este pacote.
