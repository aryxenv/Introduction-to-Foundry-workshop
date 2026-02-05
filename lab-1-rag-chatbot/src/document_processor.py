"""
Document processor for RAG pipeline
Handles loading and chunking documents from various formats
"""
import os
from typing import List, Dict, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentChunk:
    """Represents a chunk of a document"""
    
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata
    
    def __repr__(self):
        return f"DocumentChunk(content='{self.content[:50]}...', metadata={self.metadata})"


class DocumentProcessor:
    """Process documents for RAG pipeline"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor
        
        Args:
            chunk_size: Target size for text chunks (in characters)
            chunk_overlap: Overlap between chunks to preserve context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_text_file(self, file_path: str) -> str:
        """Load content from a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return ""
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If not at the end, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                sentence_endings = ['. ', '! ', '? ', '\n\n']
                best_break = end
                
                for ending in sentence_endings:
                    pos = text.rfind(ending, start, end + 100)
                    if pos != -1 and pos > start + 100:  # Ensure meaningful chunk
                        best_break = pos + len(ending)
                        break
                
                end = best_break
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = len(chunks)
                chunk_metadata['start_pos'] = start
                chunk_metadata['end_pos'] = end
                
                chunks.append(DocumentChunk(chunk_text, chunk_metadata))
            
            # Move to next chunk with overlap
            start = end - self.chunk_overlap
            
            # Ensure we make progress
            if start <= chunks[-1].metadata['start_pos'] if chunks else False:
                start = end
        
        return chunks
    
    def process_file(self, file_path: str) -> List[DocumentChunk]:
        """
        Process a single file
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            List of DocumentChunk objects
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []
        
        # Basic metadata
        metadata = {
            'source': file_path.name,
            'file_path': str(file_path),
            'file_type': file_path.suffix
        }
        
        # Load content based on file type
        if file_path.suffix in ['.txt', '.md']:
            content = self.load_text_file(str(file_path))
        else:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return []
        
        # Chunk the content
        chunks = self.chunk_text(content, metadata)
        
        logger.info(f"Processed {file_path.name}: {len(chunks)} chunks created")
        
        return chunks
    
    def process_directory(self, directory_path: str) -> List[DocumentChunk]:
        """
        Process all supported files in a directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of DocumentChunk objects from all files
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory}")
            return []
        
        all_chunks = []
        supported_extensions = ['.txt', '.md']
        
        # Find all supported files
        files = [f for f in directory.rglob('*') if f.suffix in supported_extensions]
        
        logger.info(f"Found {len(files)} documents to process")
        
        # Process each file
        for file_path in files:
            chunks = self.process_file(str(file_path))
            all_chunks.extend(chunks)
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        
        return all_chunks


def main():
    """Demo: Process documents from the knowledge base directory"""
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # Process all documents in the knowledge base
    knowledge_base_path = Path(__file__).parent.parent / "data" / "knowledge_base"
    chunks = processor.process_directory(str(knowledge_base_path))
    
    # Display results
    print(f"\n📊 Processing Summary:")
    print(f"Total chunks: {len(chunks)}")
    
    if chunks:
        print(f"\n📄 Sample chunk:")
        sample = chunks[0]
        print(f"Content: {sample.content[:200]}...")
        print(f"Metadata: {sample.metadata}")


if __name__ == "__main__":
    main()
