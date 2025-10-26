# 🚀 Despliegue en Vercel - BugHunter Shop

## ✅ Archivos de Configuración Creados

Tu proyecto ya está **listo para desplegar** en Vercel. Se han creado/modificado estos archivos:

- ✅ `vercel.json` - Configuración específica de Vercel
- ✅ `build_files.sh` - Script de construcción
- ✅ `requirements.txt` - Actualizado con dependencias para producción
- ✅ `settings.py` - Configurado para producción
- ✅ `generate_secret_key.py` - Generador de claves secretas
- ✅ `.gitignore` - Actualizado para proyectos Django

## 🚀 Pasos para Desplegar

### 1. Generar Nueva SECRET_KEY
```bash
python generate_secret_key.py
```
**¡Guarda esta clave!** La necesitarás en Vercel.

### 2. Subir a GitHub
```bash
git init
git add .
git commit -m "Ready for Vercel deployment"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sandwich-shop.git
git push -u origin main
```

### 3. Desplegar en Vercel

#### Opción A: Desde la Web de Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Conecta tu cuenta de GitHub
3. Importa tu repositorio
4. Configuración automática (Vercel detectará Django)

#### Opción B: Con Vercel CLI
```bash
npm i -g vercel
vercel login
vercel --prod
```

### 4. Variables de Entorno en Vercel
En el dashboard de Vercel, configura:

| Variable | Valor |
|----------|-------|
| `SECRET_KEY` | Tu clave generada con `generate_secret_key.py` |
| `DEBUG` | `False` |

### 5. Base de Datos (Opcional pero Recomendado)

#### Opción A: Railway (Recomendada)
1. Ve a [railway.app](https://railway.app)
2. Crea proyecto → Add PostgreSQL
3. Copia la `DATABASE_URL`
4. Añádela como variable de entorno en Vercel

#### Opción B: Supabase
1. Ve a [supabase.com](https://supabase.com)
2. Crea proyecto → Settings → Database
3. Usa la connection string como `DATABASE_URL`

### 6. Archivos de Media (Opcional)

#### Para imágenes de productos:
```bash
pip install django-cloudinary-storage
```

En `settings.py` añadir:
```python
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'tu-cloud-name',
    'API_KEY': 'tu-api-key', 
    'API_SECRET': 'tu-api-secret',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

## 🎯 URLs Finales

Una vez desplegado tendrás:
- **Sitio web**: `https://tu-proyecto.vercel.app`
- **Admin panel**: `https://tu-proyecto.vercel.app/admin/`

## 🔧 Solución de Problemas

### Build Error
```bash
# Si falla el build, verifica localmente:
python manage.py collectstatic --noinput
python manage.py check --deploy
```

### 500 Error
- Verifica variables de entorno
- Revisa que `ALLOWED_HOSTS` esté configurado
- Chequea los logs en Vercel

### Admin no funciona
```bash
# Crear superusuario después del despliegue:
# (necesitarás acceso a la BD externa)
python manage.py createsuperuser
```

## ⚡ Comandos de Desarrollo

```bash
# Probar configuración de producción localmente
python manage.py runserver --settings=sandwich_shop.settings

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar configuración para deploy  
python manage.py check --deploy

# Ejecutar migraciones
python manage.py migrate
```

## 🎨 Personalización Post-Despliegue

### Dominio personalizado
1. En Vercel → Settings → Domains
2. Añade tu dominio
3. Actualiza `ALLOWED_HOSTS` en `settings.py`

### HTTPS (Automático)
Vercel proporciona HTTPS automáticamente ✅

### CDN (Automático) 
Vercel incluye CDN global ✅

## 📊 Monitoreo

- **Analytics**: Disponible en Vercel dashboard
- **Logs**: Función logs en tiempo real
- **Performance**: Métricas integradas

## 🔄 Actualizaciones

Cada push a `main` desplegará automáticamente:
```bash
git add .
git commit -m "Actualización"
git push origin main
```

## 💡 Mejores Prácticas

1. **Nunca subas** `.env` o claves secretas a GitHub
2. **Usa** base de datos externa para producción
3. **Configura** almacenamiento externo para archivos media
4. **Mantén** `DEBUG=False` en producción
5. **Actualiza** `ALLOWED_HOSTS` con tu dominio

## 🆘 Soporte

¿Problemas? Contacta:
- 📧 miguelzamudioolsin@gmail.com  
- 🐙 GitHub: [ELANONIMOGG](https://github.com/ELANONIMOGG)

---

## 🎉 ¡Tu tienda ya está lista para el mundo!

Con esta configuración tendrás:
- ✅ Deploy automático
- ✅ HTTPS incluido
- ✅ CDN global 
- ✅ Escalado automático
- ✅ Monitoreo integrado

**¡Felicitaciones! 🎊 Tu BugHunter Shop estará online en minutos.**