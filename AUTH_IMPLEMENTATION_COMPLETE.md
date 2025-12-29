# Authentication Integration - Quick Implementation Guide

## Changes Made to Backend ✅

1. ✅ Added authentication dependencies to `requirements-mock.txt`
2. ✅ Created `server/core/auth_utils.py` - JWT tokens & password hashing  
3. ✅ Created `server/core/user_storage.py` - JSON file user database
4. ✅ Created `server/routers/auth.py` - Register/Login API endpoints
5. ✅ Updated `server/mock_server.py` - Integrated auth router, protected /generate
6. ✅ Created `server/data/users.json` - User storage file
7. ✅ Created backup system & persistent storage config

## Frontend Components Created ✅

1. ✅ `client/hooks/useAuth.ts` - Authentication state management
2. ✅ `client/components/auth/AuthModal.tsx` - Login/Register UI

## Integration into Studio.tsx (MANUAL STEPS NEEDED)

### Step 1: Add imports (top of file)
```typescript
import AuthModal from '../auth/AuthModal';
import { useAuth } from '@/hooks/useAuth';
```

### Step 2: Add auth state (inside Studio component, line ~35)
```typescript
// Authentication
const { isAuthenticated, token, login, register } = useAuth();
const [showAuthModal, setShowAuthModal] = useState(false);
```

### Step 3: Modify handleGenerate function (line ~151)
```typescript
const handleGenerate = async () => {
    // ... existing validation ...
    
    // ADD THIS CHECK
    if (!isAuthenticated || !token) {
        setShowAuthModal(true);
        return;
    }
    
    // ... rest of function ...
    
    // MODIFY axios.post to include token
    const response = await axios.post(`${API_URL}/api/v1/generate`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
```

### Step 4: Add AuthModal component (before closing </div>, line ~503)
```tsx
{/* Authentication Modal */}
<AuthModal
  isOpen={showAuthModal}
  onClose={() => setShowAuthModal(false)}
  onSuccess={() => {
    setShowAuthModal(false);
    setTimeout(() => handleGenerate(), 500);
  }}
  onLogin={login}
  onRegister={register}
/>
```

## Testing Flow

1. Fill video generation form
2. Click "Generate Video"
3. If not logged in → Auth modal appears
4. User registers/logs in  
5. Modal closes
6. Video generation proceeds automatically
7. JWT token included in API request
8. Backend validates token and creates job

## Data Persistence

- Users stored in `server/data/users.json`
- Render persistent disk configured (see `RENDER_PERSISTENT_DISK.md`)
- Encrypted backups can be committed to GitHub
- `.gitignore` updated to protect sensitive data

## Security

- Passwords hashed with bcrypt  
- JWT tokens expire in 24 hours
- Phone number validation
- Email validation
- Thread-safe file operations

## Next Steps

1. Manually integrate auth into Studio.tsx (follow steps above)
2. Test locally
3. Build frontend: `cd client && npm run build`
4. Commit all changes
5. Push to GitHub
6. Verify on Render (auto-deploys)
7. Upload frontend to Hostinger
