# Django-Marketplace

A full-stack marketplace example with a Django + DRF backend and a React (Vite + TypeScript) frontend.

## Quick links

- **Quick start:** [QUICK_START.md](QUICK_START.md)
- **Documentation index:** [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Frontend guide:** [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
- **Frontend summary & checklist:** [FRONTEND_SUMMARY.md](FRONTEND_SUMMARY.md) · [FRONTEND_IMPLEMENTATION_CHECKLIST.md](FRONTEND_IMPLEMENTATION_CHECKLIST.md)
- **Technical summary:** [TECHNICAL_SUMMARY.md](TECHNICAL_SUMMARY.md)
- **Implementation notes:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) · [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
- **What was built:** [WHAT_WAS_BUILT.md](WHAT_WAS_BUILT.md)
- **Commands & quick reference:** [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) · [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Marketplace README (extra):** [MARKETPLACE_README.md](MARKETPLACE_README.md)
- **Frontend local README:** [Frontend/README.md](Frontend/README.md)

## Local development (backend)

1. Create & activate virtualenv (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Apply migrations and run server:

```powershell
cd Backend
python manage.py migrate
python manage.py runserver
```

Static files are collected to `Backend/staticfiles` when you run `collectstatic`.

## Local development (frontend)

1. Install and run the Vite dev server:

```bash
cd Frontend
npm install
npm run dev
```

2. The frontend expects the backend API at `http://127.0.0.1:8000/api/v1` by default. Edit `Frontend/src/services/api.ts` to change the base URL if needed.

## Notes

- Protected backend routes will redirect to login; create a superuser with `python manage.py createsuperuser` to access the admin and add sample data.
- See `DOCUMENTATION_INDEX.md` for a full list of project docs and developer notes.

---

If you want, I can tidy and centralize the docs into a single `docs/` folder and update links accordingly.

