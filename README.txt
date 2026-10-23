GPT Roku Backend

1. Suba estes arquivos em um servidor Python (ex.: Render).
2. Configure a variável OPENAI_API_KEY com sua chave da OpenAI.
3. Opcional: OPENAI_MODEL=gpt-6-astra.
4. Depois do deploy, copie a URL HTTPS, por exemplo:
   https://meu-gpt-roku.onrender.com/ask
5. No app Roku, edite components/MainScene.brs e substitua:
   https://SEU-SERVIDOR/ask
   pela URL real.
6. Recompacte o conteúdo do app com o arquivo manifest na raiz.
