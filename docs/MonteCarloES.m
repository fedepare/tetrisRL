clc;
clear all
close all

% Possible actions:

%actionList      = (-5:1:5)';

actionList      = (-50:10:50)';

    
N               = 100;

% Q               = zeros(N,size(actionList,1));

Q               = rand(N,size(actionList,1));

Returns         = cell(N,size(actionList,1));

Policy          = randi(size(actionList,1),N,1);

for Episode = 1:1000
    
    % Episode:
    episodeLength       = 100;
    
    stateActionHistory  = zeros(episodeLength,2);
    rewardHistory       = zeros(episodeLength,1);
        
        
    % Start at random state:
    state           = randi(N,1,1);
    
    for k=1:episodeLength
        
        % Action according to current policy:
        actionIdx           = Policy(state);
        
        % Random action
        %actionIdx = randi(size(actionList,1),1);
        
        action              = actionList(actionIdx);
        
        newState            = state + action;
        
        reward              = 1-1/50*abs(50-newState);
        
        if newState>N
            state = N;
        elseif newState<1
            state = 1;
        else
            state = newState; 
        end 
        
        stateActionHistory(k,:) = [state,actionIdx];
        
        rewardHistory(k,1)    = reward;
        
    end
    
    % Shorter notation:
    sAH = stateActionHistory;
    
    for i=1:episodeLength
        
        % Find state-action combinations:
        stateIndex  = sAH(:,1)==sAH(i,1);
        actionIndex = sAH(:,2)==sAH(i,2);
        
        sIdx        = find(stateIndex & actionIndex);
        
        % Take the first time we see the state-action combination:
        sIdx        = sIdx(1);
        
        % Sum of all future rewards:
        R           = sum(rewardHistory(sIdx:end,1));
        
        Returns{sAH(i,1),sAH(i,2)}  = [Returns{sAH(i,1),sAH(i,2)};R];
        
        % Update state-action values:
        Q(sAH(i,1),sAH(i,2))        = mean(Returns{sAH(i,1),sAH(i,2)});
        
        % Update Policy:
        if rand<1
            Policy(sAH(i,1))        = randi(size(actionList,1),1,1);
        else
            [~,Policy(sAH(i,1))]    = max(Q(sAH(i,1),:));
        end
    end
end

% Plot Q:
figure
surf(flipud(Q))
xlabel('Action','FontSize',18,'FontWeight','bold')
ylabel('State','FontSize',18,'FontWeight','bold')
zlabel('Q','FontSize',18,'FontWeight','bold')

