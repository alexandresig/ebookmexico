# Progresso da montagem — versão GPT Image

## Versão vigente

As imagens de MX-F001 a MX-F005 foram **geradas com GPT Image**, pela ferramenta `image_gen`, e substituem os desenhos por código entregues anteriormente. A versão anterior permanece no commit `9d45c02` e no histórico da branch; não refazer ou apagar esse histórico.

- Fonte do ebook: `Ebook_Codex_corrigido.zip`; 160 páginas e 104 campos. ZIP antigo ignorado.
- Originais do gerador, sem retoques por código: `imagens/originais_gpt/MX-F001.png` a `MX-F005.png`.
- PNGs finais: `imagens/MX-F001.png` a `MX-F005.png`, com tamanho dos prompts. O único processamento por código é adequação proporcional de resolução e margem branca, sem redesenho de textos, componentes ou conexões.
- Ilustrações 1, 2 e 5 representam equipamentos reconhecíveis; esquemas 3 e 4 também foram gerados com GPT Image, conforme a correção solicitada pelo usuário. A arte inclui volume/perspectiva em equipamentos, afastando-se do estilo estritamente plano dos prompts originais para atender ao pedido de imagens ilustradas do usuário.
- O script `scripts/produzir_bloco_001_005.py` é histórico da versão antiga, desenhada por código; **não usá-lo para sobrescrever as imagens atuais**. `scripts/preparar_imagens_gpt.py` apenas prepara os PNGs já gerados e incorpora um por vez.

| Código | Página | Origem | Criada | Conferida | Inserida | Bloqueada |
|---|---:|---|---|---|---|---|
| MX-F001 | 4 | GPT Image | sim | sim | sim | não |
| MX-F002 | 9 | GPT Image | sim | sim | sim | não |
| MX-F003 | 10 | GPT Image | sim | sim | sim | não |
| MX-F004 | 10 | GPT Image | sim | sim | sim | não |
| MX-F005 | 12 | GPT Image | sim | sim | sim | não |

## Conferência desta versão

- MX-F001: representações ilustradas dos dois quadros, luminárias, contatos e motor/bomba; duas setas residenciais e uma industrial, sem misturar as funções.
- MX-F002: depósito e tubulação inferior com válvula regulável; associações pressão/tensão, vazão/corrente e restrição/resistência, com a nota de limite do modelo.
- MX-F003: conferência visual do percurso + → H1 → H2 → − e das duas ramas independentes em paralelo; pontos nas derivações, sem ponte direta entre polos ou ligação entre os circuitos.
- MX-F004: conferência visual de S0 NC e FR1 NC antes da bifurcação; S1 NA em paralelo apenas com auxiliar KM1 NA 13-14; retorno da bobina A2 a 0 V. Sem KS1 ou união com PE. Não houve simulação elétrica nem ensaio físico.
- MX-F005: primeira geração revisada pelo próprio GPT Image para trocar a aparência de botão de emergência por pulsador vermelho de paro normal. Oito blocos e sequência funcional preservados, KM1 associado por rótulos e tensões qualificadas como exemplos.
- As cinco gerações e a correção foram inspecionadas visualmente. Não foram detectados textos cortados, conexões indevidas ou identificadores trocados nesta revisão; os equipamentos ilustrados são representações conceituais, sem pretensão de reproduzir bornes de um fabricante.
- HTML verificado no Chromium: 160 páginas, 104 campos e 5 imagens preenchidas; dimensões nativas carregadas correspondem aos PNGs finais; referências, substituição, importação em lote, download e acionamento de impressão passaram, sem erros JavaScript. Páginas 4, 9, 10 e 12 capturadas e inspecionadas após montagem. PDF de produção não gerado.
- Comparação com o ZIP corrigido: CSS, scripts, bases de página e todos os bytes fora dos cinco campos permanecem idênticos. As outras 99 figuras continuam pendentes.

Nenhuma figura bloqueada neste bloco. Conferência didática visual, sem certificação para instalação real. A próxima execução deve avançar para **MX-F006 a MX-F010**, usando GPT Image e preservando este progresso.
