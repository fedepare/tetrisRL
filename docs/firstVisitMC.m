clc;
clear all
close all

N               = 100;
V               = zeros(N,1);
Returns         = cell(N,1);

for Episode = 1:50
    
    stateHistory    = zeros(100,1);
    rewardHistory   = zeros(100,1);
    
    % Episode:
    episodeLength   = 500;
    
    % Start halfway:
    state           = floor(N/2);
    
    % Start at 1:
    state           = 1;
    
    for k=1:episodeLength
        
        % Deterministic action +1
        action              = 1;
        
        % Random action -5/+5:
        %action              = round(rand*10-5);
        
        % Random action 0/10:
        %action              = floor(rand*10);
                
        newState            = state + action;
        
        %reward              = newState/N-0.5;
        
        %reward              = 1-1/50*abs(50-newState);
        reward              = (newState>20 && newState<30); 
            
        
        if newState>N
            state = N;
        elseif newState<1
            state = 1;
        else
            state = newState; 
        end 
        
        stateHistory(k,1)   = state;
        
        rewardHistory(k,1)  = reward;
        
    end
    
    for i=1:episodeLength
        sIdx                        = find(stateHistory==stateHistory(i));
        
        sIdx                        = sIdx(1);
        
        %R                           = sum(rewardHistory(sIdx:end,1));
        
        % Mean of obtained rewards:
        R                           = sum(rewardHistory(sIdx:end,1)) / length(rewardHistory(sIdx:end,1));
        
        Returns{stateHistory(i)}    =  [Returns{stateHistory(i)};R];
        
        V(stateHistory(i))          = mean(Returns{stateHistory(i)});
    end
end

plot(V,'LineWidth',3)
set(gca,'FontSize',14,'FontWeight','bold')
xlabel('State','FontSize',18,'FontWeight','bold')
ylabel('V(s)','FontSize',18,'FontWeight','bold')