# Day2で実装: OpenAI Whisper API で音声→テキスト変換
# from openai import AsyncOpenAI
# client = AsyncOpenAI()


async def transcribe_audio(audio_url: str) -> str:
    """
    音声URLを受け取りWhisperで文字起こしする。
    Day1はスタブ（空文字列を返す）。
    Day2実装予定:
      1. audio_urlからバイナリをダウンロード
      2. openai.audio.transcriptions.create() に渡す
      3. テキストを返す
    """
    return ""
