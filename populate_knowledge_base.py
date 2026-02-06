"""
Populate ChromaDB vector store with curriculum examples.
Run this once to initialize the knowledge base.
"""
import os
import glob
from src.rag.vector_store import CurriculumVectorStore


def load_curriculum_documents():
    """Load all curriculum documents from knowledge base."""
    documents = []
    metadatas = []
    ids = []
    
    # Load ML curricula
    ml_files = glob.glob("data/knowledge_base/ml_curricula/*.md")
    for filepath in ml_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            
            # Extract metadata from filename and content
            filename = os.path.basename(filepath)
            if 'masters' in filename.lower():
                level = 'Masters'
                subject = 'Machine Learning'
            elif 'btech' in filename.lower():
                level = 'BTech'
                subject = 'Artificial Intelligence'
            else:
                level = 'Unknown'
                subject = 'ML/AI'
            
            metadatas.append({
                'source': filepath,
                'level': level,
                'subject': subject,
                'category': 'ml_ai'
            })
            ids.append(f"ml_{filename.replace('.md', '')}")
    
    # Load Web Dev curricula
    web_files = glob.glob("data/knowledge_base/web_dev_curricula/*.md")
    for filepath in web_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            
            filename = os.path.basename(filepath)
            metadatas.append({
                'source': filepath,
                'level': 'Certification',
                'subject': 'Web Development',
                'category': 'web_dev'
            })
            ids.append(f"web_{filename.replace('.md', '')}")
    
    # Load templates
    template_files = glob.glob("data/knowledge_base/templates/*.md")
    for filepath in template_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            
            filename = os.path.basename(filepath)
            metadatas.append({
                'source': filepath,
                'level': 'Template',
                'subject': 'Generic',
                'category': 'template'
            })
            ids.append(f"template_{filename.replace('.md', '')}")
    
    return documents, metadatas, ids


def main():
    """Initialize vector store with curriculum examples."""
    print("🚀 Initializing Curriculum Knowledge Base...")
    print("=" * 60)
    
    # Initialize vector store
    vector_store = CurriculumVectorStore()
    
    # Clear existing data (optional - comment out to keep existing data)
    if vector_store.get_count() > 0:
        print(f"\n⚠ Found {vector_store.get_count()} existing documents")
        response = input("Clear existing data? (y/n): ")
        if response.lower() == 'y':
            vector_store.clear()
            print("✓ Cleared existing data")
    
    # Load documents
    print("\n📚 Loading curriculum documents...")
    documents, metadatas, ids = load_curriculum_documents()
    print(f"✓ Loaded {len(documents)} documents")
    
    # Add to vector store
    print("\n💾 Adding documents to vector store...")
    vector_store.add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("\n" + "=" * 60)
    print("✅ Knowledge base initialized successfully!")
    print(f"   Total documents: {vector_store.get_count()}")
    print(f"   Storage location: {vector_store.persist_directory}")
    print("\nYou can now run the Streamlit app: streamlit run app.py")


if __name__ == "__main__":
    main()
