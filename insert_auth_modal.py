import sys

# Read Studio.tsx
with open('client/components/studio/Studio.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the location to insert (before the last 3 closing divs)
# Looking for the pattern of closing divs before the closing brace
insert_line = None
for i in range(len(lines) - 1, 0, -1):
    if '</div>' in lines[i] and i < len(lines) - 5:
        # Found a good spot - before the last few closing divs
        insert_line = i + 1
        break

if not insert_line:
    print("ERROR: Could not find insertion point")
    sys.exit(1)

# AuthModal component to insert
auth_modal = '''
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
'''

# Insert the component
new_lines = lines[:insert_line] + [auth_modal] + lines[insert_line:]

# Write back
with open('client/components/studio/Studio.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✅ Successfully added AuthModal at line {insert_line}")
print(f"📝 Total lines: {len(lines)} -> {len(new_lines)}")
