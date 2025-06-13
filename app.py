
from supabase import create_client, Client
import os

# Thông tin kết nối Supabase (cần thay bằng thông tin thật nếu deploy)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================== CUỘC HỌP ==================
def insert_cuoc_hop(ten, ngay, gio, noidung, tep):
    supabase.table("cuoc_hop").insert({
        "ten": ten,
        "ngay": ngay.strftime("%d/%m/%y"),
        "gio": gio.strftime("%H:%M"),
        "noidung": noidung,
        "tep": tep
    }).execute()

def get_cuoc_hop():
    res = supabase.table("cuoc_hop").select("*").order("ngay", desc=True).execute()
    return res.data if res.data else []

def delete_cuoc_hop(id):
    supabase.table("cuoc_hop").delete().eq("id", id).execute()

# ================== NHẮC VIỆC ==================
def insert_nhac_viec(viec, ngay, gio, email):
    supabase.table("nhac_viec").insert({
        "viec": viec,
        "ngay": ngay.strftime("%d/%m/%y"),
        "gio": gio.strftime("%H:%M"),
        "email": email
    }).execute()

def get_nhac_viec():
    res = supabase.table("nhac_viec").select("*").order("ngay", desc=True).execute()
    return res.data if res.data else []

def delete_nhac_viec(id):
    supabase.table("nhac_viec").delete().eq("id", id).execute()
