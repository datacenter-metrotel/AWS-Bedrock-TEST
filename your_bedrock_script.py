import boto3
import json
from botocore.exceptions import ClientError

# --- ¡ADVERTENCIA DE SEGURIDAD CRÍTICA PARA ESTE LABORATORIO! ---
# Estas claves se insertan DIRECTAMENTE en el código. Esto es SOLO para un
# laboratorio de PRUEBA DE FUNCIONALIDAD MUY ESPECÍFICA y EFÍMERA.
#
# ACCIÓN URGENTE REQUERIDA DESPUÉS DE LA PRUEBA:
# DEBES ELIMINAR ESTAS CLAVES DE ACCESO DE TU CUENTA DE AWS INMEDIATAMENTE.
# No las uses en ningún otro script ni las guardes.
# --- ¡FIN DE LA ADVERTENCIA! ---

# Tus credenciales proporcionadas para el laboratorio.
AWS_ACCESS_KEY_ID_LAB = "XXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY_LAB = "XXXXXXXXXXXXXXXXXX"
AWS_SESSION_TOKEN_LAB = None 

def chat_with_bedrock_sonnet(
    region: str = 'us-east-1',
    model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'
) -> None:
    """
    Inicia una sesión de chat interactiva con el modelo Claude 3 Sonnet en Bedrock (On-Demand).
    Mantiene el contexto de la conversación.
    """
    try:
        # Crea el cliente de Bedrock Runtime usando las credenciales directamente
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=region,
            aws_access_key_id=AWS_ACCESS_KEY_ID_LAB,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY_LAB,
            aws_session_token=AWS_SESSION_TOKEN_LAB
        )
        
        print("--- INICIANDO CHAT INTERACTIVO CON CLAUDE 3 SONNET (Modo On-Demand, Credenciales Directas) ---")
        print(f"Modelo: {model_id} en {region}")
        print("Escribe 'salir' o 'exit' para terminar la conversación.")
        print("-" * 80)

        # Lista para mantener el historial de la conversación
        messages = []

        while True:
            user_input = input("\nTú: ").strip()

            if user_input.lower() in ("salir", "exit"):
                print("--- Finalizando la conversación. ---")
                break

            # Añadir el mensaje del usuario al historial
            messages.append({"role": "user", "content": [{"type": "text", "text": user_input}]})

            try:
                # Prepara el cuerpo de la solicitud con el historial completo
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": messages # Enviamos todo el historial aquí
                }
                
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    contentType='application/json',
                    accept='application/json',
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                
                # Extrae el contenido de la respuesta del modelo
                if 'content' in response_body and len(response_body['content']) > 0 and 'text' in response_body['content'][0]:
                    generated_text = response_body['content'][0]['text']
                    print(f"Claude: {generated_text}")
                    # Añadir la respuesta del asistente al historial
                    messages.append({"role": "assistant", "content": [{"type": "text", "text": generated_text}]})
                else:
                    print(f"Claude: (Error al extraer la respuesta. Detalles: {response_body})")
                    # No añadir al historial si no se pudo extraer la respuesta
            
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code")
                print(f"\n--- ERROR DURANTE LA INTERACCIÓN ---")
                if error_code == "AccessDeniedException":
                    print(f"Error de Acceso Denegado: Las credenciales no tienen permisos para 'bedrock:InvokeModel' o el acceso al modelo está restringido. Verifica tu política de IAM.")
                elif error_code == "ValidationException":
                    print(f"Error de Validación: El 'model_id' o el formato de la solicitud no son correctos. Detalles: {e}")
                elif error_code == "ResourceNotFoundException":
                    print(f"Error de Recurso No Encontrado: El modelo '{model_id}' no está disponible o no está habilitado en tu cuenta en la región '{region}'.")
                else:
                    print(f"Error de Cliente Inesperado: {e}")
                print("Por favor, corrige el problema e intenta de nuevo o sal del chat.")
                # Si hay un error, no añadimos la respuesta vacía al historial para evitar enredos.
            except Exception as e:
                print(f"\n--- ERROR INESPERADO DURANTE LA INTERACCIÓN ---")
                print(f"Detalles: {e}")
                print("Por favor, corrige el problema e intenta de nuevo o sal del chat.")
                # Si hay un error, no añadimos la respuesta vacía al historial para evitar enredos.

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        print(f"\n--- ERROR AL INICIAR LA CONEXIÓN A BEDROCK ---")
        if error_code == "AccessDeniedException":
            print(f"Error de Acceso Denegado: Asegúrate de que las credenciales codificadas sean válidas y tengan los permisos mínimos para iniciar el cliente de Bedrock.")
        else:
            print(f"Error de Cliente Inesperado al iniciar: {e}")
    except Exception as e:
        print(f"\n--- ERROR INESPERADO AL INICIAR LA CONEXIÓN ---")
        print(f"Detalles: {e}")

if __name__ == "__main__":
    # --- Configuración para la Sesión de Chat ---
    BEDROCK_REGION_CHAT = 'us-east-1'
    # ID del modelo para Anthropic Claude 3 Sonnet (On-Demand)
    BEDROCK_MODEL_ID_CHAT = 'anthropic.claude-3-sonnet-20240229-v1:0' 

    # Inicia el chat
    chat_with_bedrock_sonnet(
        region=BEDROCK_REGION_CHAT,
        model_id=BEDROCK_MODEL_ID_CHAT
    )

    print("\n--- SESIÓN DE CHAT FINALIZADA ---")
    print("¡RECUERDA ELIMINAR LAS CLAVES DE ACCESO DE TU CUENTA AWS AHORA MISMO PARA TU SEGURIDAD!")
