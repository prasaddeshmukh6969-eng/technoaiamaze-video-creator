// Add to Studio.tsx after line 210 (at the end of the component, before closing div)

{/* Authentication Modal */}
<AuthModal
  isOpen={showAuthModal}
  onClose={() => setShowAuthModal(false)}
  onSuccess={() => {
    setShowAuthModal(false);
    // Automatically retry generation after successful auth
    setTimeout(() => handleGenerate(), 500);
  }}
  onLogin={login}
  onRegister={register}
/>
