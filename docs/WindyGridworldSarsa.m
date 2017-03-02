clc;
clear all
close all

alpha   = 0.5;
gamma   = 0.9;
eps     = 0;

% Possible actions:
UP              = 1;
DOWN            = 2;
RIGHT           = 3;
LEFT            = 4;
actionList      = [UP;DOWN;RIGHT;LEFT];

WIND            = [0,0,0,1,1,1,2,2,1,0];
STARTSTATE      = [4,1];
GOALSTATE       = [4,8];

Nver            = 7;   % Number of states in vertical direction
Nhor            = 10;  % Number of states in horizontal direction

Q               = zeros(Nver,Nhor,size(actionList,1));

Policy          = randi(size(actionList,1),Nver,Nhor);
allK            = zeros(300,1);

for Episode = 1:300
    
    % Episode:
    episodeLength       = 100;
    
    % Start at random state:
    state           	= STARTSTATE;
    
    % Action according to current policy:
    actionIdx           = Policy(state(1,1),state(1,2));
    
    action              = actionList(actionIdx);
    
    for k=1:episodeLength
        
        if state(1,1)==GOALSTATE(1,1) && state(1,2)==GOALSTATE(1,2)
            allK(Episode) = k-1; % reached previous timestep
            break
        end
        
        % Update state:
        newState = state;
        
        if action==UP
            
            newState(1,1) = newState(1,1)-1;
            
        elseif action==DOWN
            
            newState(1,1) = newState(1,1)+1;
            
        elseif action==LEFT
            
            newState(1,2) = newState(1,2)-1;
            
        elseif action==RIGHT
            
            newState(1,2) = newState(1,2)+1;
            
        else
            error('Unkmown action')
        end
        
        % Wind effects:
        newState(1,1) = newState(1,1)-WIND(state(1,2));
        
        % Out if bounds checking:
        if newState(1,1)<1
            newState(1,1)=1;
        end
        if newState(1,1)>Nver
            newState(1,1)=Nver;
        end
        if newState(1,2)<1
            newState(1,2)=1;
        end
        if newState(1,2)>Nhor
            newState(1,2)=Nhor;
        end
        
        % Reward:
        if newState(1,1)==GOALSTATE(1,1) && newState(1,2)==GOALSTATE(1,2)
            reward=1;
        else
            reward=-1;
        end
        
        % Action according to current policy:
        newActionIdx       = Policy(newState(1,1),newState(1,2));
        
        newAction          = actionList(newActionIdx);
        
        % Update state-action values:
        Q(state(1,1),state(1,2),actionIdx) = Q(state(1,1),state(1,2),actionIdx)+alpha*(reward+gamma*Q(newState(1,1),newState(1,2),newActionIdx)-Q(state(1,1),state(1,2),actionIdx));
        
        % Update Policy:
        if rand<eps
            Policy(state(1,1),state(1,2))     = randi(size(actionList,1),1,1);
        else
            dummy(:,:)                        = Q(state(1,1),state(1,2),:);
            [~,Policy(state(1,1),state(1,2))] = max(dummy);
            clear dummy;
        end
        
        % Update state and action:
        state               = newState;
        
        actionIdx           = newActionIdx;
        
        action              = newAction;
        
    end
    if state(1,1)~=GOALSTATE(1,1) || state(1,2)~=GOALSTATE(1,2)
        allK(Episode) = episodeLength;
    end
    
end

Policy


% Plot Q:
% figure
% surf(Q)
% xlabel('Action','FontSize',18,'FontWeight','bold')
% ylabel('State','FontSize',18,'FontWeight','bold')
% zlabel('Q','FontSize',18,'FontWeight','bold')
% title('SARSA','FontSize',18,'FontWeight','bold')

figure
plot(allK)

xlabel('Episode','FontSize',18,'FontWeight','bold')
ylabel('Number of steps to goal','FontSize',18,'FontWeight','bold')

%Plot Value Function and policy
% [V,I] = max(Q,[],3);
% 
% figure
% surf(V)
% 
% figure
% surf(I)

