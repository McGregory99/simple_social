import streamlit as st
import requests
import json
import base64
import urllib.parse

st.set_page_config(page_title="Social Media App", layout="wide")

# Initialize session state 
if 'token' not in st.session_state:
    st.session_state.token = None

if 'user' not in st.session_state:
    st.session_state.user = None

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

API_URL = "http://localhost:8000"


def auth_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def register_user(email: str, password: str):
    payload = {"email": email, "password": password}
    return requests.post(f"{API_URL}/auth/register", json=payload)


def login_user(email: str, password: str):
    data = {"username": email, "password": password}
    return requests.post(f"{API_URL}/auth/jwt/login", data=data)


def upload_post(caption: str, file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    data = {"caption": caption}
    return requests.post(f"{API_URL}/upload", headers=auth_headers(), files=files, data=data)


def fetch_feed():
    return requests.get(f"{API_URL}/feed", headers=auth_headers())


def render_auth_page():
    st.title("Autenticación")
    st.caption("Elige iniciar sesión o registrarte para continuar")

    col_login, col_register = st.columns(2)
    with col_login:
        if st.button("Login", use_container_width=True):
            st.session_state.auth_mode = "login"
    with col_register:
        if st.button("Registrarse", use_container_width=True):
            st.session_state.auth_mode = "register"

    st.divider()
    if st.session_state.auth_mode == "login":
        st.subheader("Iniciar sesión")
        log_email = st.text_input("Email", key="log_email")
        log_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Entrar", type="primary"):
            resp = login_user(log_email, log_pass)
            if resp.ok:
                token = resp.json().get("access_token")
                st.session_state.token = token
                st.session_state.user = log_email
                st.success("Sesión iniciada")
                st.rerun()
            else:
                st.error(f"Login fallido: {resp.text}")
    else:
        st.subheader("Crear cuenta")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Registrar", type="primary"):
            resp = register_user(reg_email, reg_pass)
            if resp.ok:
                st.success("Usuario creado. Ahora inicia sesión.")
                st.session_state.auth_mode = "login"
            else:
                st.error(f"Error al registrar: {resp.text}")


def render_app():
    st.title("Social Media App")

    with st.sidebar:
        st.success(f"Sesión: {st.session_state.user}")
        if st.button("Cerrar sesión"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

    st.subheader("Subir post")
    caption = st.text_area("Caption")
    file = st.file_uploader("Archivo (imagen o video)")
    if st.button("Subir", type="primary"):
        if not file or not caption:
            st.warning("Completa caption y archivo.")
        else:
            resp = upload_post(caption, file)
            if resp.ok:
                st.success("Post subido")
            else:
                st.error(f"Error al subir: {resp.text}")

    st.subheader("Feed")
    if st.button("Actualizar feed"):
        st.rerun()

    resp = fetch_feed()
    if resp.ok:
        posts = resp.json()
        if not posts:
            st.write("No hay posts aún.")
        for post in posts:
            with st.container():
                st.markdown(f"**Caption:** {post.get('caption')}")
                st.markdown(f"**Tipo:** {post.get('file_type')} | **Archivo:** {post.get('file_name')} | **Creado:** {post.get('created_at')}")
                # Mostrar media si es imagen o video
                url = post.get("url")
                if post.get("file_type", "").startswith("image"):
                    st.image(url, width=320)  # mostrar más pequeño
                elif post.get("file_type", "").startswith("video"):
                    st.video(url)
                else:
                    st.markdown(f"[Ver contenido]({url})")

                if post.get("is_owner"):
                    if st.button("🗑️", key=f"del-{post.get('id')}"):
                        delete_resp = requests.delete(f"{API_URL}/posts/{post.get('id')}", headers=auth_headers())
                        if delete_resp.ok:
                            st.success("Post eliminado")
                            st.rerun()
                        else:
                            st.error(f"No se pudo eliminar: {delete_resp.text}")
                st.divider()
    else:
        st.error(f"No se pudo obtener el feed: {resp.text}")


if not st.session_state.token:
    render_auth_page()
else:
    render_app()
