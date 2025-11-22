import time
from app.services.extractor import extract_graph_from_text
from app.services.graph_store import save_graph_to_neo4j

# YOUR DATASET
dummy_articles = [
    {"title": "OpenAI Board Fires Sam Altman",
        "summary": "In a stunning move, OpenAI's board has removed Sam Altman as CEO, citing lack of candor."},
    {"title": "Microsoft Hires Sam Altman",
        "summary": "Satya Nadella announced Sam Altman will head Microsoft's new advanced AI research division."},
    {"title": "Sam Altman Returns to OpenAI",
        "summary": "After internal turmoil, Sam Altman is reinstated as OpenAI CEO with a restructured board."},

    # --- Duplicates / Variants (The Stress Test) ---
    {"title": "Sam Altman Fired by OpenAI Board",
        "summary": "OpenAI dismissed CEO Sam Altman due to concerns about transparency."},
    {"title": "Satya Nadella Brings Sam Altman to Microsoft",
        "summary": "Microsoft hires former OpenAI CEO Sam Altman to lead a new AI research division."},

    # --- New News ---
    {"title": "Nvidia Unveils Blackwell B200 GPU",
        "summary": "The Blackwell B200 promises massive improvements in AI inference performance."},
    {"title": "Elon Musk Sues OpenAI",
        "summary": "Elon Musk claims OpenAI deviated from its original nonprofit mission."},
    {"title": "Apple Introduces Apple Intelligence",
        "summary": "Apple enters the AI race with deep integration of generative models into iOS and macOS."},
    {"title": "The New York Times Sues Microsoft and OpenAI",
        "summary": "NYT alleges mass copyright violation from training language models."},

    # --- Repeat Variant ---
    {"title": "Nvidia Reveals B200 Blackwell",
        "summary": "CEO Jensen Huang announces the new GPU for advanced AI."},
    {
        "title": "Microsoft and OpenAI Strengthen AI Partnership",
        "summary": "After recent leadership turbulence, Microsoft deepens its collaboration with OpenAI to accelerate AI research."
    },
    {
        "title": "OpenAI CEO Altman Discusses Future of AGI",
        "summary": "Sam Altman shared insights about OpenAI’s plans for AGI development in a recent interview."
    },
    {
        "title": "Jensen Huang Talks About Blackwell Architecture",
        "summary": "The Nvidia CEO explained how the Blackwell architecture will redefine AI compute efficiency."
    },
    {
        "title": "New GPU Rumored: Nvidia’s B200X Variant Leaks",
        "summary": "Leaks suggest Nvidia is preparing an even faster version of the Blackwell B200 series."
    },
    {
        "title": "OpenAI Board Addresses Firing Controversy",
        "summary": "OpenAI's board released a brief statement but did not clarify the exact reasons for Sam Altman's removal."
    },
    {
        "title": "Microsoft Expands Hiring Spree for AI Talent",
        "summary": "Microsoft continues to hire AI researchers, following the addition of Sam Altman."
    },
    {
        "title": "Elon Musk Criticizes OpenAI on Social Media",
        "summary": "Musk posted that OpenAI had strayed from its original mission, deepening his conflict with the organization."
    },
    {
        "title": "Apple Intelligence Will Compete with OpenAI Models",
        "summary": "Analysts believe Apple Intelligence aims to challenge models like GPT and Claude."
    },
    {
        "title": "NYT vs OpenAI Legal Battle Intensifies",
        "summary": "The New York Times expanded its lawsuit, adding further allegations of misuse."
    },
    {
        "title": "Sam Altman Speaks at Microsoft HQ",
        "summary": "Altman discussed future AI initiatives during his brief time at Microsoft."
    },
    {
        "title": "Meta Develops Llama 4 Turbo Variant",
        "summary": "Meta is reportedly testing a faster version of Llama 4 for enterprise clients."
    },
    {
        "title": "Google DeepMind Teases Gemini Ultra Mode",
        "summary": "DeepMind hinted at a new mode in Gemini designed for long-context reasoning."
    },
    {
        "title": "Nvidia Partners with Tesla for AI Training",
        "summary": "Tesla announced a collaboration with Nvidia to improve training efficiency for its robotics models."
    },
    {
        "title": "Tesla Optimus Robot Demonstrates New Learning Abilities",
        "summary": "Optimus showed improved balance and manipulation in a new demo."
    },
    {
        "title": "Anthropic Expands Claude Model Family",
        "summary": "Claude 4.1 Mini and Claude 4.1 Pro Max were revealed as part of a scaling strategy."
    },
    {
        "title": "IBM Granite LLM Gains Enterprise Adoption",
        "summary": "More enterprises are adopting IBM’s Granite LLM due to its safety-first approach."
    },
    {
        "title": "OpenAI Announces New Safety Committees",
        "summary": "OpenAI revealed new oversight groups aimed at ensuring responsible AGI development."
    },
    {
        "title": "Microsoft Faces Pressure Over NYT Lawsuit",
        "summary": "Legal experts say Microsoft may face secondary liability in the copyright case."
    },
    {
        "title": "Blackwell B200 Benchmarks Leak Online",
        "summary": "Early benchmarks show significant gains over the previous H100 hardware."
    },
    {
        "title": "Confusion Over Altman's Role After Reinstatement",
        "summary": "Some reports claim Altman gained more power, while others say his influence decreased."
    }
]


def run_simulation():
    print("🚀 STARTING SMART SIMULATION (DEDUPLICATION TEST)...")
    print(f"Loaded {len(dummy_articles)} articles.")
    print("--------------------------------------------------")

    for i, article in enumerate(dummy_articles):
        print(
            f"\n📄 Processing {i+1}/{len(dummy_articles)}: '{article['title']}'")

        full_text = f"{article['title']}. {article['summary']}"

        try:
            # 1. Extract
            print("   🧠 Llama 3 Extracting & Normalizing...")
            graph_data = extract_graph_from_text(full_text)

            if graph_data:
                # Debug: Show what the LLM decided the ID should be
                # This lets you see if it normalized "Samuel" to "Sam"
                node_ids = [n.id for n in graph_data.nodes]
                print(f"   🔍 Extracted Entities: {node_ids}")

                # 2. Save (MERGE logic handles the deduplication)
                print("   💾 Saving to Neo4j (Merging duplicates)...")
                save_graph_to_neo4j(graph_data)
                print("   ✅ Done.")
            else:
                print("   ⚠️ No data extracted.")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        # Fast sleep for testing
        time.sleep(1)

    print("\n--------------------------------------------------")
    print("🎉 SIMULATION COMPLETE.")


if __name__ == "__main__":
    run_simulation()
