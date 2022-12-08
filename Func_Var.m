function [EDP_Var, zero_damp_xi, delta] = Func_Var(story, mu, sigma, rho, Gamman, Eigvec, h)

% An: the 𝑛th modens effective participation factor for the EDP
An = zeros(story);
for mode=1:story
    for story = 1:story
        if story == 1
            An(mode,story) = Gamman(mode)*(Eigvec(story,mode))/h;
        else
            An(mode,story) = Gamman(mode)*(Eigvec(story,mode)-Eigvec(story-1,mode))/h;
        end
    end
end

% SRSS
% first order approximation
max_s = zeros(story,1);
for ii=1:story
    for k=1:story
        max_s(ii,1) = max_s(ii,1) + An(k,ii)^2 * mu(k)^2;
    end
end
max_s = sqrt(max_s);
max_story = find(max_s == max(max_s));

% Note that when the peak value of the 𝑑th story's IDR is selected as the EDP,
% the effective participation factor 𝐴𝑛 is calculated based on the assumption
% that the maximum IDR occurs at the same story for any ground motions applied
An = An(:,max_story);
sr = max_s(max_story);

% Derive the EDP residuals of building structures
% Equation (21) in the reference paper
EDP_Var = 0;
for k=1:story-1
    EDP_Var = EDP_Var + (An(k)^2*mu(k)/sr)^2 * sigma(k)^2;
end
for k=1:story-1
    for l=k+1:story
        EDP_Var = EDP_Var + 2 * An(k)^2*mu(k)/sr * An(l)^2*mu(l)/sr * sigma(k) * sigma(l) * rho(k,l);
    end
end

% Equation (24) in the reference paper
delta = sqrt(EDP_Var)/abs(sr);
zero_damp_xi = sqrt(log(1+delta^2));