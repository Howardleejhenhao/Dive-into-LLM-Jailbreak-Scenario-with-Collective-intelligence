document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'https://ai.back.driseam.com'; // Adjust if your backend runs elsewhere
    const TOKEN_KEY = 'llm_game_auth_token';


    const authSection = document.getElementById('auth-section');
    const loginFormContainer = document.getElementById('login-form-container');
    const registerFormContainer = document.getElementById('register-form-container');
    const userInfoDiv = document.getElementById('user-info');
    const loggedInUsernameSpan = document.getElementById('logged-in-username');

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const challengeForm = document.getElementById('challenge-form');
    const attackForm = document.getElementById('attack-form');

    const showRegisterBtn = document.getElementById('show-register-btn');
    const showLoginBtn = document.getElementById('show-login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const selectAttackerBtn = document.getElementById('select-attacker');
    const selectDefenderBtn = document.getElementById('select-defender');
    const backToRolesDefenderBtn = document.getElementById('back-to-roles-defender');
    const backToRolesAttackerBtn = document.getElementById('back-to-roles-attacker');
    const retryChallengeBtn = document.getElementById('retry-challenge-btn');
    const quitGameBtn = document.getElementById('quit-game-btn');
    const viewLeaderboardsBtn = document.getElementById('view-leaderboards-btn');
    const backToRolesLeaderboardBtn = document.getElementById('back-to-roles-leaderboard'); 
    const viewUserLeaderboardBtn = document.getElementById('view-user-leaderboard-btn'); 
    const backToRolesUserLeaderboardBtn = document.getElementById('back-to-roles-user-leaderboard');

    const roleSelection = document.getElementById('role-selection');
    const defenderSection = document.getElementById('defender-section');
    const attackerSection = document.getElementById('attacker-section');
    const challengeListDiv = document.getElementById('challenge-list');
    const gamePlaySection = document.getElementById('game-play-section');
    const gameOverControls = document.getElementById('game-over-controls');
    const leaderboardSection = document.getElementById('leaderboard-section'); 
    const overallLeaderboardContent = document.getElementById('overall-leaderboard-content'); 
    const userLeaderboardSection = document.getElementById('user-leaderboard-section'); 
    const userLeaderboardContent = document.getElementById('user-leaderboard-content'); 

    const forbiddenWordsInput = document.getElementById('forbidden-words'); 
    const forbiddenSentenceCount = document.getElementById('forbidden-sentence-count'); 

    const attackerModelSelectionDiv = document.getElementById('attacker-model-selection-div'); 

    const modelBtnGroup = document.createElement('div');
    modelBtnGroup.className = 'model-btn-group';
    const modelBtn1 = document.createElement('button');
    modelBtn1.type = 'button';
    modelBtn1.className = 'model-btn active';
    modelBtn1.textContent = 'Gemini 1.5 Flash';
    modelBtn1.dataset.model = 'models/gemini-1.5-flash';
    const modelBtn2 = document.createElement('button');
    modelBtn2.type = 'button';
    modelBtn2.className = 'model-btn';
    modelBtn2.textContent = 'Gemini 2.0 Flash';
    modelBtn2.dataset.model = 'models/gemini-2.0-flash';
    modelBtnGroup.appendChild(modelBtn1);
    modelBtnGroup.appendChild(modelBtn2);
    if (attackerModelSelectionDiv) {
        attackerModelSelectionDiv.innerHTML = '<label>Select model you want to challenge:</label>';
        attackerModelSelectionDiv.appendChild(modelBtnGroup);
    }

    let currentModelFilter = 'models/gemini-1.5-flash';

    [modelBtn1, modelBtn2].forEach(btn => {
        btn.addEventListener('click', () => {
            [modelBtn1, modelBtn2].forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentModelFilter = btn.dataset.model;
            loadChallenges(currentModelFilter);
        });
    });

    const playingCreatorUsernameSpan = document.getElementById('playing-creator-username'); 
    const playingForbiddenWordsSpan = document.getElementById('playing-forbidden-words');
    const turnsLeftSpan = document.getElementById('turns-left');
    const chatHistoryDiv = document.getElementById('chat-history');
    const attackMessageInput = document.getElementById('attack-message');
    const attackMessageCount = document.getElementById('attack-message-count'); 
    const playingDescriptionSpan = document.getElementById('playing-description'); 

    let currentChallenge = null; 
    let currentGameId = null; 
    let currentUser = null; 
    let isAllowedUser = false; 

    if (forbiddenWordsInput && forbiddenSentenceCount) {
        forbiddenWordsInput.addEventListener('input', () => {
            const maxLength = 50;
            let currentValue = forbiddenWordsInput.value;
            if (currentValue.length > maxLength) {
                currentValue = currentValue.substring(0, maxLength);
                forbiddenWordsInput.value = currentValue;
            }
            forbiddenSentenceCount.textContent = `${currentValue.length}/${maxLength}`;
        });
        forbiddenSentenceCount.textContent = `${forbiddenWordsInput.value.length}/50`;
    }


    function getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    function setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    }

    function removeToken() {
        localStorage.removeItem(TOKEN_KEY);
    }

    async function fetchWithAuth(url, options = {}) {
        const token = getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        let body = options.body;
        if (options.body instanceof URLSearchParams) {
            headers['Content-Type'] = 'application/x-www-form-urlencoded';
        } else if (typeof body === 'object' && !(body instanceof FormData) && !(body instanceof URLSearchParams)) {
            body = JSON.stringify(body);
        }

        const response = await fetch(url, { ...options, headers, body });

        if (response.status === 401) { 
            handleLogout(); 
            alert("Session expired or invalid. Please log in again.");
            throw new Error("Unauthorized");
        }
        return response;
    }
    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    function formatConversation(conversation) {
        let html = '<div class="conversation">'; 
        conversation.forEach(turn => {
            const role = turn.role;
            const text = turn.parts && turn.parts[0] ? turn.parts[0].text : '[empty message]';
            const className = role === 'user' ? 'user-message' : 'assistant-message';
            html += `<p class="${className}"><strong>${role === 'user' ? 'Attacker' : 'Defender'}:</strong> ${escapeHtml(text)}</p>`;
        });
        html += '</div>';
        return html;
    }
    function updateAuthUI() {
        if (currentUser) {
            authSection.classList.add('hidden'); 
            userInfoDiv.classList.remove('hidden'); 
            loggedInUsernameSpan.textContent = currentUser;
            roleSelection.classList.remove('hidden'); 
            
            if (isAllowedUser) {
                selectDefenderBtn.classList.remove('hidden');
            } else {
                selectDefenderBtn.classList.add('hidden');
                
                if (defenderSection && !defenderSection.classList.contains('hidden')) {
                    defenderSection.classList.add('hidden');
                }
            }

        } else {
            
            authSection.classList.remove('hidden');
            loginFormContainer.classList.remove('hidden');
            registerFormContainer.classList.add('hidden');
            userInfoDiv.classList.add('hidden'); 

            
            roleSelection.classList.add('hidden');
            defenderSection.classList.add('hidden');
            attackerSection.classList.add('hidden');
            gamePlaySection.classList.add('hidden');
            leaderboardSection.classList.add('hidden'); 
            userLeaderboardSection.classList.add('hidden'); 
        }
    }

    function showSection(sectionToShow) {
        console.log(`[showSection] Called to show: ${sectionToShow ? sectionToShow.id : 'null'}`);
        const allSections = [
            roleSelection,
            defenderSection,
            attackerSection,
            leaderboardSection, 
            userLeaderboardSection, 
            authSection 
        ];

        allSections.forEach(section => {
            if (section) {
                if (!section.classList.contains('hidden')) {
                    section.classList.add('hidden');
                }
            }
        });

        if (sectionToShow !== attackerSection) {
            if (challengeListDiv) challengeListDiv.classList.remove('hidden');
            if (gamePlaySection) gamePlaySection.classList.add('hidden');
            if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.add('hidden'); 
        } else {
            if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.remove('hidden');
            if (challengeListDiv) challengeListDiv.classList.remove('hidden');
            if (gamePlaySection) gamePlaySection.classList.add('hidden');
        }
        if (gameOverControls) gameOverControls.classList.add('hidden');

        if (sectionToShow === attackerSection && gamePlaySection && !gamePlaySection.classList.contains('hidden')) {
            if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.add('hidden');
        }

        if (sectionToShow === defenderSection && !isAllowedUser) {
            console.warn("[showSection] Attempt to show defenderSection for non-allowed user. Aborting and showing role selection.");
            if (currentUser) { 
                roleSelection.classList.remove('hidden');
            } else { 
                authSection.classList.remove('hidden');
            }
            return; 
        }
        if (sectionToShow) {
            sectionToShow.classList.remove('hidden');
            console.log(`[showSection] Final class list for ${sectionToShow.id}:`, sectionToShow.classList);
        } else {
            if (!currentUser && authSection) {
                authSection.classList.remove('hidden');
            }
        }
    }

    function addChatMessage(role, content) {
        const p = document.createElement('p');
        p.classList.add(`${role}-message`);
        p.textContent = content;
        chatHistoryDiv.appendChild(p);
        chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight; 
    }


    async function handleLogin(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_BASE_URL}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, 
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
                throw new Error(errorData.detail || 'Login failed');
            }

            const data = await response.json();
            setToken(data.access_token);
            await checkLoginStatus(); 

            if (currentUser) {
                showSection(roleSelection); 
                loginForm.reset();
            } else {
                throw new Error("Failed to verify user after login.");
            }

        } catch (error) {
            console.error('Login error:', error);
            alert(`Login failed: ${error.message}`);
            handleLogout(); 
        }
    }

    async function handleRegister(event) {
        event.preventDefault();
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, hashed_password: password }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
                throw new Error(errorData.detail || 'Registration failed');
            }

            alert('Registration successful! Please log in.');
            registerForm.reset();
            registerFormContainer.classList.add('hidden');
            loginFormContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Registration error:', error);
            alert(`Registration failed: ${error.message}`);
        }
    }

    function handleLogout() {
        removeToken();
        currentUser = null;
        currentChallenge = null;
        currentGameId = null; 
        isAllowedUser = false;
        updateAuthUI();
    }

    async function checkLoginStatus() {
        const token = getToken();
        isAllowedUser = false; 
        if (token) {
            try {
                const userResponse = await fetchWithAuth(`${API_BASE_URL}/users/me`);
                if (!userResponse.ok) {
                    const errorData = await userResponse.json().catch(() => ({}));
                    throw new Error(errorData.detail || `Failed to verify token (Status: ${userResponse.status})`);
                }
                const userData = await userResponse.json();
                currentUser = userData.username;

                try {
                    const permResponse = await fetchWithAuth(`${API_BASE_URL}/users/me/permissions`);
                    if (!permResponse.ok) {
                        console.error(`Failed to fetch permissions (Status: ${permResponse.status})`);
                        const errorDetail = await permResponse.json().catch(() => ({}));
                        // alert(`Could not load user permissions: ${errorDetail.detail || permResponse.statusText}`);
                    } else {
                        const permData = await permResponse.json();
                        isAllowedUser = permData.is_allowed;
                        console.log(`User ${currentUser} allowed status: ${isAllowedUser}`);
                    }
                } catch (permError) {
                    console.error("Error fetching permissions:", permError);
                    // Avoid double alert if permError is "Unauthorized" as fetchWithAuth handles it
                    // if (permError.message !== "Unauthorized") {
                    //     alert("An error occurred while fetching user permissions.");
                    // }
                    // isAllowedUser remains false
                }

            } catch (error) {
                console.error("Token validation or initial data load failed:", error.message);
                if (error.message === "Unauthorized") {
                } else {
                    currentUser = null; 
                }
            }
        } else {
            currentUser = null;
        }
        updateAuthUI();
    }

    challengeForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(challengeForm);
        const data = {
            defender_prompt: formData.get('defender_prompt'),
            forbidden_words: formData.get('forbidden_words'),
            description: formData.get('description')
        };

        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/challenges`, {
                method: 'POST',
                body: data, 
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Failed to create challenge' }));
                throw new Error(errorData.detail || 'Failed to create challenge');
            }

            alert('Challenge created successfully!');
            challengeForm.reset();
            showSection(roleSelection); 
        } catch (error) {
            console.error('Error creating challenge:', error);
            if (error.message !== "Unauthorized") {
                alert(`Error creating challenge: ${error.message}`);
            }
        }
    });


    async function loadChallenges(filterModel = '') { 
        challengeListDiv.innerHTML = 'Loading challenges...';
        let url = `${API_BASE_URL}/challenges`;
        if (filterModel) {
            url += `?model=${encodeURIComponent(filterModel)}`;
        }

        try {
            const response = await fetchWithAuth(url); 
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to load challenges');
            }
            const challenges = await response.json(); 

            if (challenges.length === 0) {
                challengeListDiv.innerHTML = 'No challenges available yet.';
                return;
            }

            challengeListDiv.innerHTML = '';
            challenges.forEach(challenge => {
                const div = document.createElement('div');
                div.classList.add('challenge-item');
                const MAX_WINS = 10; 
                const isPlayable = challenge.successful_attacks < MAX_WINS;
                const modelDisplayName = challenge.model.startsWith('models/') ? challenge.model.substring(7) : challenge.model;
                const descriptionHtml = escapeHtml(challenge.description).replace(/\n/g, '<br>');
                const solvedMarkup = challenge.solved_by_current_user ? 
                    '<span class="solved-checkmark">✓</span>' : '';
                //<p><strong>Forbidden Words:</strong> ${escapeHtml(challenge.forbidden_words)}</p>
                div.innerHTML = `
                    <p><strong>Creator:</strong> ${escapeHtml(challenge.creator_username)}</p>
                    <p><strong>Model:</strong> ${escapeHtml(modelDisplayName)}</p>
                    <p><strong>Description:</strong> ${descriptionHtml}</p>
                    <p><strong>Wins:</strong> ${challenge.successful_attacks} / ${MAX_WINS}</p>
                    ${challenge.category ? `<p><strong>Category:</strong> ${escapeHtml(challenge.category)}</p>` : ''}
                    ${solvedMarkup}
                    <button data-challenge-id="${challenge.id}" ${!isPlayable ? 'disabled class="disabled-play"' : ''}>
                        ${isPlayable ? 'Play' : 'Completed'}
                    </button>
                `;
                if (isPlayable) {
                    div.querySelector('button').addEventListener('click', () => startGame(challenge));
                }
                challengeListDiv.appendChild(div);
            });
        } catch (error) {
            console.error('Error loading challenges:', error);
            if (error.message !== "Unauthorized") {
                challengeListDiv.innerHTML = `Error loading challenges: ${error.message}`;
            }
        }
    }

    function startGame(challenge) {
        currentChallenge = challenge;
        currentGameId = null;
        showSection(attackerSection);
        challengeListDiv.classList.add('hidden');
        gamePlaySection.classList.remove('hidden');
        chatHistoryDiv.innerHTML = '';
        gameOverControls.classList.add('hidden');
        if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.add('hidden');

        playingCreatorUsernameSpan.textContent = challenge.creator_username;
        const descriptionHtml = escapeHtml(challenge.description || '').replace(/\n/g, '<br>');
        playingDescriptionSpan.innerHTML = descriptionHtml; 
        playingForbiddenWordsSpan.textContent = `${challenge.forbidden_words}`;
        turnsLeftSpan.textContent = '10';
        chatHistoryDiv.innerHTML = '<p class="system-message">Game started vs. ' + challenge.creator_username + '. Try to make the AI say the forbidden words!</p>'; 

        console.log('startGame called with challenge:', challenge);
        console.log('Updating playing-description with:', challenge.description);
        if (!playingDescriptionSpan) {
            console.error('playingDescriptionSpan element not found in DOM');
        } else {
            playingDescriptionSpan.innerHTML = descriptionHtml;
        }

        attackMessageInput.disabled = false;
        attackMessageInput.value = '';
        attackForm.querySelector('button').disabled = false; 
        attackForm.classList.remove('hidden'); 
        attackMessageInput.focus();
    }

    attackForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 
        await handleAttackSubmit(); 
    });

    attackMessageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
            event.preventDefault(); 
            attackForm.querySelector('button[type="submit"]').click();
        }
    });

    if (attackMessageInput && attackMessageCount) {
        attackMessageInput.addEventListener('input', () => {
            const maxLength = 500;
            let currentValue = attackMessageInput.value;
            if (currentValue.length > maxLength) {
                currentValue = currentValue.substring(0, maxLength);
                attackMessageInput.value = currentValue;
            }
            attackMessageCount.textContent = `${currentValue.length}/${maxLength}`;
        });
        attackMessageCount.textContent = `${attackMessageInput.value.length}/500`;

        attackForm.addEventListener('submit', () => {
            attackMessageCount.textContent = '0/500';
        });
    }

    async function handleAttackSubmit() {
        if (!currentChallenge) return;

        const message = attackMessageInput.value.trim();
        if (!message) return;

        addChatMessage('user', message);
        attackMessageInput.value = '';
        attackMessageInput.disabled = true; 
        attackForm.querySelector('button').disabled = true;

        const requestBody = { message: message };
        if (currentGameId) {
            requestBody.game_id = currentGameId;
        }

        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/play/attack/${currentChallenge.id}`, {
                method: 'POST',
                body: requestBody, 
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Failed to parse error response' }));
                
                
                if (response.status === 403 || response.status === 404) {
                    addChatMessage('system', `Error: ${errorData.detail || 'Challenge/Game session issue.'}`);
                    attackForm.classList.add('hidden'); 
                    gameOverControls.classList.remove('hidden'); 
                    retryChallengeBtn.classList.add('hidden'); 
                    quitGameBtn.textContent = 'Back to Challenge List'; 
                    currentGameId = null; 
                    return;
                }
                throw new Error(errorData.detail || `Failed to send message (Status: ${response.status})`);
            }

            const result = await response.json();

            currentGameId = result.game_id;

            addChatMessage('assistant', result.response);

            if (result.status === 'game_over') {
                let endMessage = `Game Over! Winner: ${result.winner}. Reason: ${result.reason}`;
                addChatMessage('system', endMessage);

                if (currentChallenge) {
                     currentChallenge.successful_attacks = result.challenge_wins;
                }

                attackForm.classList.add('hidden');
                gameOverControls.classList.remove('hidden');

                const MAX_WINS = 10; 
                if (result.winner === 'defender' && currentChallenge && result.challenge_wins < MAX_WINS) {
                    retryChallengeBtn.classList.remove('hidden');
                } else {
                    retryChallengeBtn.classList.add('hidden'); 
                }
                quitGameBtn.textContent = 'Back to Challenge List'; 
                currentGameId = null;

            } else {
                turnsLeftSpan.textContent = result.turns_left;
                attackMessageInput.disabled = false;
                attackForm.querySelector('button').disabled = false;
                attackMessageInput.focus();
            }
        } catch (error) {
            console.error('Error during attack turn:', error);
            if (error.message !== "Unauthorized") { 
                addChatMessage('system', `Error: ${error.message}`);
            }
            const responseStatus = error.response ? error.response.status : null;
            if (error.message !== "Unauthorized" && ![403, 404].includes(responseStatus)) {
                attackMessageInput.disabled = false;
                attackForm.querySelector('button').disabled = false;
            } else { 
                attackForm.classList.add('hidden');
                gameOverControls.classList.remove('hidden');
                retryChallengeBtn.classList.add('hidden');
                quitGameBtn.textContent = 'Back to Challenge List';
                currentGameId = null; 
            }
        }
    }


    async function loadChallengeLeaderboard() { 
        overallLeaderboardContent.innerHTML = '<p class="loading">Loading challenge leaderboard...</p>'; 
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/leaderboard/overall`);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to load challenge leaderboard'); 
            }
            const overallData = await response.json(); 
            renderChallengeLeaderboard(overallData);
        } catch (error) {
            console.error('Error loading challenge leaderboard:', error); 
            if (error.message !== "Unauthorized") {
                overallLeaderboardContent.innerHTML = `<p class="error">Error loading challenge leaderboard: ${escapeHtml(error.message)}</p>`; 
            }
        }
    }

    function renderChallengeLeaderboard(overallData) {
        if (!overallData || overallData.length === 0) {
            overallLeaderboardContent.innerHTML = '<p>No challenges found or no successful attacks recorded yet.</p>';
            return;
        }

        let html = '';
        overallData.forEach((challenge, challengeIndex) => {
            let displayDescription;
            if (challenge.description === null || challenge.description === undefined) {
                displayDescription = 'N/A';
            } else {
                displayDescription = challenge.description; 
            }
            const escapedDescription = escapeHtml(displayDescription);
            const descriptionWithLineBreaks = escapedDescription.replace(/\n/g, '<br>'); 

            const creatorUsername = escapeHtml(challenge.creator_username || 'Unknown');

            let modelString;
            if (challenge.model === null || challenge.model === undefined) {
                modelString = 'N/A';
            } else {
                modelString = challenge.model; 
            }
            
            let modelDisplayName = modelString;
            if (modelString && modelString !== 'N/A' && modelString.startsWith('models/')) {
                modelDisplayName = modelString.substring(7);
            }
            const escapedModel = escapeHtml(modelDisplayName);

            html += `
                <div class="leaderboard-challenge-entry">
                    <h4>Description: ${descriptionWithLineBreaks}</h4>
                    <p><strong>Creator:</strong> ${creatorUsername}</p>
                    <p><strong>Model:</strong> ${escapedModel}</p>
            `; 

            if (challenge.successful_attacks && Array.isArray(challenge.successful_attacks) && challenge.successful_attacks.length > 0) {
                html += `<p><strong>Successful Attacks (${challenge.successful_attacks.length}):</strong></p>`;
                challenge.successful_attacks.forEach((attack, index) => {
                    const attackerName = escapeHtml(attack.attacker_username || 'Anonymous');
                    const turns = attack.turns !== undefined && attack.turns !== null ? attack.turns : '?';
                    const conversationHtml = attack.conversation && Array.isArray(attack.conversation) ? formatConversation(attack.conversation) : '<p class="error">[Conversation data unavailable]</p>';

                    html += `
                        <details class="leaderboard-attack-entry">
                            <summary>
                                <strong>Success #${index + 1}</strong> by ${attackerName} (${turns} turns) - Click to view conversation
                            </summary>
                            ${conversationHtml}
                        </details>
                    `;
                });
            } else {
                html += `<p>No successful attacks recorded for this challenge.</p>`;
            }

            html += `</div>`; 

            if (challengeIndex < overallData.length - 1) {
                html += '<hr class="leaderboard-separator">';
            }
        });
        overallLeaderboardContent.innerHTML = html;
    }

    async function loadUserLeaderboard() {
        userLeaderboardContent.innerHTML = '<p class="loading">Loading user leaderboard...</p>';
        try {
            const response = await fetchWithAuth(`${API_BASE_URL}/leaderboard/users`);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to load user leaderboard');
            }
            const userData = await response.json();
            renderUserLeaderboard(userData);
        } catch (error) {
            console.error('Error loading user leaderboard:', error);
            if (error.message !== "Unauthorized") {
                userLeaderboardContent.innerHTML = `<p class="error">Error loading user leaderboard: ${escapeHtml(error.message)}</p>`;
            }
        }
    }

    function renderUserLeaderboard(userData) {
        if (!userData || userData.length === 0) {
            userLeaderboardContent.innerHTML = '<p>No users have solved any challenges yet.</p>';
            return;
        }

        let html = '<ol class="user-leaderboard-list">';
        userData.forEach((userEntry) => {
            const username = escapeHtml(userEntry.username || 'Unknown');
            const challengesSolved = userEntry.challenges_solved;
            html += `
                <li class="user-leaderboard-entry">
                    <span class="leaderboard-username">${username}</span>
                    <span class="leaderboard-score">${challengesSolved} solved</span>
                </li>
            `;
        });
        html += '</ol>';
        userLeaderboardContent.innerHTML = html;
    }

    // --- Event Listeners ---

    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    logoutBtn.addEventListener('click', handleLogout);

    showRegisterBtn.addEventListener('click', () => {
        loginFormContainer.classList.add('hidden');
        registerFormContainer.classList.remove('hidden');
    });

    showLoginBtn.addEventListener('click', () => {
        registerFormContainer.classList.add('hidden');
        loginFormContainer.classList.remove('hidden');
    });

    selectAttackerBtn.addEventListener('click', () => {
        showSection(attackerSection);
        currentModelFilter = 'models/gemini-1.5-flash';
        modelBtn1.classList.add('active');
        modelBtn2.classList.remove('active');
        loadChallenges(currentModelFilter);
    });

    selectDefenderBtn.addEventListener('click', () => {
        showSection(defenderSection);
    });

    backToRolesDefenderBtn.addEventListener('click', () => showSection(roleSelection));
    backToRolesAttackerBtn.addEventListener('click', () => {
        showSection(roleSelection);
        currentChallenge = null;
        currentGameId = null;
        gamePlaySection.classList.add('hidden');
        challengeListDiv.classList.remove('hidden');
        if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.add('hidden');
    });

    // Use the renamed quitGameBtn ID from HTML
    quitGameBtn.addEventListener('click', () => {
        currentChallenge = null;
        currentGameId = null;
        showSection(attackerSection);
        gamePlaySection.classList.add('hidden');
        challengeListDiv.classList.remove('hidden');
        if (attackerModelSelectionDiv) attackerModelSelectionDiv.classList.remove('hidden');
        loadChallenges(currentModelFilter);
    });

    // Retry button listener
    retryChallengeBtn.addEventListener('click', () => {
        if (currentChallenge) {
            startGame(currentChallenge);
        }
    });

    // Challenge Leaderboard Button
    viewLeaderboardsBtn.addEventListener('click', () => {
        console.log("Challenge Leaderboard button clicked.");
        if (!leaderboardSection) {
            console.error("Cannot show challenge leaderboard: leaderboardSection element not found!");
            alert("Error: Challenge leaderboard section element is missing.");
            return;
        }
        try {
            showSection(leaderboardSection);
            loadChallengeLeaderboard(); 
        } catch (error) {
             console.error("Error in challenge leaderboard button click handler:", error);
             alert("Could not display the challenge leaderboard section due to an error.");
        }
    });

    // Back button for Challenge Leaderboard
    backToRolesLeaderboardBtn.addEventListener('click', () => {
        showSection(roleSelection);
    });

    // User Leaderboard Button (New)
    viewUserLeaderboardBtn.addEventListener('click', () => {
        console.log("User Leaderboard button clicked.");
        if (!userLeaderboardSection) {
            console.error("Cannot show user leaderboard: userLeaderboardSection element not found!");
            alert("Error: User leaderboard section element is missing.");
            return;
        }
        try {
            showSection(userLeaderboardSection);
            loadUserLeaderboard();
        } catch (error) {
             console.error("Error in user leaderboard button click handler:", error);
             alert("Could not display the user leaderboard section due to an error.");
        }
    });

    backToRolesUserLeaderboardBtn.addEventListener('click', () => {
        showSection(roleSelection);
    });

    checkLoginStatus(); 

});