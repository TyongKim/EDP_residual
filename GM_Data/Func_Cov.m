function EDP_Cov = Func_Cov(story_i, story_j, mu_i, mu_j, sigma_i, sigma_j, rho_ij, Gamman_i, Gamman_j, Eigvec_i, Eigvec_j, h_i, h_j)

% An: the 𝑛th modens effective participation factor for the EDP
An_i = zeros(story_i);
for mode=1:story_i
    for story = 1:story_i
        if story == 1
            An_i(mode,story) = Gamman_i(mode)*(Eigvec_i(story,mode))/h_i;
        else
            An_i(mode,story) = Gamman_i(mode)*(Eigvec_i(story,mode)-Eigvec_i(story-1,mode))/h_i;
        end
    end
end

An_j = zeros(story_j);
for mode=1:story_j
    for story = 1:story_j
        if story == 1
            An_j(mode,story) = Gamman_j(mode)*(Eigvec_j(story,mode))/h_j;
        else
            An_j(mode,story) = Gamman_j(mode)*(Eigvec_j(story,mode)-Eigvec_j(story-1,mode))/h_j;
        end
    end
end

% SRSS
% first order approximation
max_si = zeros(story_i,1);
for ii=1:story_i
    for k=1:story_i
        max_si(ii,1) = max_si(ii,1) + An_i(k,ii)^2 * mu_i(k)^2;
    end
end
max_si = sqrt(max_si);
max_story_i = find(max_si == max(max_si));

max_sj = zeros(story_j,1);
for jj=1:story_j
    for k=1:story_j
        max_sj(jj,1) = max_sj(jj,1) + An_j(k,jj)^2 * mu_j(k)^2;
    end
end
max_sj = sqrt(max_sj);
max_story_j = find(max_sj == max(max_sj));


% Note that when the peak value of the 𝑑th story's IDR is selected as the EDP,
% the effective participation factor 𝐴𝑛 is calculated based on the assumption
% that the maximum IDR occurs at the same story for any ground motions applied
An_i = An_i(:,max_story_i);
An_j = An_j(:,max_story_j);
        
sr_i = max_si(max_story_i);
sr_j = max_sj(max_story_j);

% Equation (22) in the reference paper
EDP_Cov = 0;
for ii=1:story_i
    for jj=1:story_j
        EDP_Cov = EDP_Cov + An_i(ii)^2*mu_i(ii)/sr_i * An_j(jj)^2*mu_j(jj)/sr_j * sigma_i(ii) * sigma_j(jj) * rho_ij(ii,jj);
    end
end
