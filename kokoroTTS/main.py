import torch
import kokoroTTS

def main():
    torch.manual_seed(42)
    text = """Every company that runs software in the cloud has to answer one question. How do you create and manage all that infrastructure, the servers, the databases, the networks, without it turning into chaos? Over the years, the industry figured out a pretty good answer to that. But then, companies started growing. Teams got bigger, services multiplied, and that answer stopped being enough. In this video, we are going to look at what that problem actually looks like and how the best engineering teams in the world have learned to solve it. We'll start from the very basics of how infrastructure is managed in the cloud and work our way up to where that breaks down at scale and look at what companies actually do to fix it. Let's get started."""
    
    model = kokoroTTS.model(lang_code='a')
    
    kokoroTTS.generate(
        model=model,
        text=text,
        outputPath="output.wav",
        voice="af_heart,af_bella",
        speed=1.0
    )
    print("Audio saved successfully to output.wav")

if __name__ == "__main__":
    main()
