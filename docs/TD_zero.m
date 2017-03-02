clc;
clear all
close all

gamma           = 0.99;
alpha           = 0.1;
N               = 100;
V               = zeros(N,1);
Returns         = cell(N,1);

for Episode = 1:300
    
    stateHistory    = zeros(100,1);
    rewardHistory   = zeros(100,1);
    
    % Episode:
    episodeLength   = 100;
    
    % Start halfway:
    state           = floor(N/2);
    
    % Start at 1:
%     state           = 1;
    
    for k=1:episodeLength
        
        % Deterministic action +1
        %action              = 1;
        
        % Random action -5/+5:
        action              = round(rand*10-5);
        
        % Random action 0/10:
        %action              = floor(rand*10);
                
        newState            = state + action;
        
        %reward              = newState/N-0.5;
        
        reward              = 1-1/50*abs(50-newState);
        
%         if newState>100 || newState<1
%             reward=-1;
%         end
        
        if newState>N
            newState = N;
        elseif newState<1
            newState = 1;
        end 
       
         % update V:
        V(state)    = V(state) + alpha*(reward + gamma*V(newState)-V(state));
        
        state       = newState;
        
    end
end

plot(V,'LineWidth',3)
set(gca,'FontSize',14,'FontWeight','bold')
xlabel('State','FontSize',18,'FontWeight','bold')
ylabel('V(s)','FontSize',18,'FontWeight','bold')