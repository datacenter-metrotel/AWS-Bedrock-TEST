import boto3
from botocore.exceptions import ClientError

# Tus credenciales proporcionadas para el laboratorio.
AWS_ACCESS_KEY_ID_LAB = "XXXXXXXXXXXXXX" # REEMPLAZA si ya las eliminaste
AWS_SECRET_ACCESS_KEY_LAB = "XXXXXXXXXXXXXXXX" # REEMPLAZA si ya las eliminaste
AWS_SESSION_TOKEN_LAB = None

def list_bedrock_foundation_models(region: str = 'us-east-1'):
    """
    Lista los modelos de base disponibles en Amazon Bedrock para una región dada.
    """
    try:
        bedrock_client = boto3.client(
            'bedrock', # Nota: Usamos 'bedrock' aquí, no 'bedrock-runtime'
            region_name=region,
            aws_access_key_id=AWS_ACCESS_KEY_ID_LAB,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY_LAB,
            aws_session_token=AWS_SESSION_TOKEN_LAB
        )

        print(f"--- Listando modelos de base en la región {region} ---")
        response = bedrock_client.list_foundation_models()
        
        models = response['modelSummaries']
        
        if not models:
            print("No se encontraron modelos de base en esta región para esta cuenta.")
            return

        print("ID de Modelo disponibles (Foundation Model IDs):")
        for model in models:
            print(f"- {model['modelId']} (Provider: {model['providerName']}, Name: {model['modelName']})")
            
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        print(f"\n--- ERROR AL LISTAR MODELOS ---")
        if error_code == "AccessDeniedException":
            print("Error de Acceso Denegado: Asegúrate de que las credenciales tengan permisos para 'bedrock:ListFoundationModels'.")
        else:
            print(f"Error de Cliente Inesperado: {e}")
    except Exception as e:
        print(f"\n--- ERROR INESPERADO AL LISTAR MODELOS ---")
        print(f"Detalles: {e}")

if __name__ == "__main__":
    list_bedrock_foundation_models(region='us-east-1')
