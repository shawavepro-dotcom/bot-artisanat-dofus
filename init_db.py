import asyncpg
import os
import asyncio
import traceback

async def init_database():
    """Initialise la base de données avec les tables nécessaires."""
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("❌ DATABASE_URL non définie !")
        return False
    
    conn = None
    try:
        conn = await asyncpg.connect(dsn)
        print("✅ Connexion à la base de données établie")
        
        # Créer la table artisans avec clé primaire composite
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS artisans (
                user_id BIGINT NOT NULL,
                metier VARCHAR(50) NOT NULL,
                niveau INT NOT NULL DEFAULT 1,
                PRIMARY KEY (user_id, metier)
            )
        """)
        print("✅ Table 'artisans' créée/vérifiée avec clé primaire composite")
        
        return True
    except asyncpg.PostgresError as e:
        print(f"❌ Erreur PostgreSQL lors de l'initialisation : {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors de l'initialisation : {e}")
        traceback.print_exc()
        return False
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    success = asyncio.run(init_database())
    exit(0 if success else 1)

