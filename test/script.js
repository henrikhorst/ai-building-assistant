fetch('inquiry_log.json')
    .then(response => response.json())
    .then(data => {
        const listContainer = document.getElementById('conversationList');
        data.forEach(conversation => {
            const conversationDiv = document.createElement('div');
            conversationDiv.className = 'conversation';

            // Always get the first step
            const firstStep = conversation.steps[0];

            // Iterate over all lookups within the first step
            firstStep.lookups.forEach(lookup => {
                const lookupKey = Object.keys(lookup)[0];
                const lookupDetails = lookup[lookupKey];

                // Iterate over messages within the lookup
                lookupDetails.messages.forEach(message => {
                    const messageDiv = document.createElement('div');
                    const preElement = document.createElement('pre'); // Use pre element to preserve whitespace and format
                    preElement.style.whiteSpace = 'pre-wrap'; // Allows wrapping
                    
                    // Check the role to set the class appropriately
                    if (message.role === 'user') {
                        messageDiv.className = 'message user-message';
                        preElement.textContent = `User: ${message.content}`;
                    } else if (message.role === 'assistant' || message.role === 'system') {
                        messageDiv.className = 'message system-response';
                        preElement.textContent = `${message.role === 'assistant' ? 'Assistant' : 'System'}: ${message.content}`;
                    }

                    messageDiv.appendChild(preElement); // Append pre element to the message div
                    conversationDiv.appendChild(messageDiv);
                });
            });

            listContainer.appendChild(conversationDiv);
        });
    })
    .catch(error => console.error('Error loading conversation logs:', error));
